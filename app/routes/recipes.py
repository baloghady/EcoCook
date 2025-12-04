from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Recipe, RecipeIngredient, UserInventory, ShoppingList, ShoppingListItem
from app.extensions import db
from app.utils.unit_service import convert_recipe_to_ingredient_unit
from sqlalchemy import func

bp = Blueprint('recipes', __name__, url_prefix='/recipes')


@bp.route('/')
@login_required
def index():
    return recommend()


def get_user_inventory_ids(user_id):
    return set(i.ingredient_id for i in UserInventory.query.filter_by(user_id=user_id).all())

def get_user_inventory_map(user_id):
    """Get a map of ingredient_id -> total available quantity"""
    inventory = UserInventory.query.filter_by(user_id=user_id).all()
    inventory_map = {}
    for item in inventory:
        if item.ingredient_id in inventory_map:
            inventory_map[item.ingredient_id] += item.quantity
        else:
            inventory_map[item.ingredient_id] = item.quantity
    return inventory_map

def get_earliest_expiry_for_recipe(recipe, user_id):
    """Get the earliest expiry date for ingredients needed in this recipe"""
    from datetime import date, timedelta
    earliest = None
    
    for ri in recipe.ingredients:
        inventory_items = UserInventory.query.filter_by(
            user_id=user_id,
            ingredient_id=ri.ingredient_id
        ).all()
        
        for item in inventory_items:
            if item.expiry_date:
                if earliest is None or item.expiry_date < earliest:
                    earliest = item.expiry_date
    
    if earliest is None:
        return date.today() + timedelta(days=9999)
    
    return earliest

def get_ingredient_status(recipe, user_inventory_map):
    """Check each ingredient and return status with availability details"""
    ingredient_details = []
    for ri in recipe.ingredients:
        available_qty = user_inventory_map.get(ri.ingredient_id, 0)
        ing_unit_value = ri.ingredient.unit.value if hasattr(ri.ingredient.unit, 'value') else ri.ingredient.unit
        converted_needed = convert_recipe_to_ingredient_unit(ri.quantity, ri.unit, ing_unit_value)
        needed_qty = converted_needed if converted_needed is not None else ri.quantity
        
        status = {
            'name': ri.ingredient.name,
            'needed': needed_qty,
            'available': available_qty,
            'unit_str': ing_unit_value,
            'is_sufficient': available_qty >= needed_qty,
            'missing': max(0, needed_qty - available_qty)
        }
        ingredient_details.append(status)
    
    return ingredient_details

def get_missing_ingredients(recipe, user_ingredient_ids):
    missing = []
    for ri in recipe.ingredients:
        if ri.ingredient_id not in user_ingredient_ids:
            missing.append(ri.ingredient.name)
    return missing

def get_missing_count(recipe, user_ingredient_ids):
    return sum(1 for ri in recipe.ingredients if ri.ingredient_id not in user_ingredient_ids)

@bp.route('/recommend')
@login_required
def recommend():
    sort = request.args.get('sort', 'match')
    recipes = Recipe.query.all()
    user_inventory_map = get_user_inventory_map(current_user.id)
    recs = []
    for recipe in recipes:
        ingredient_status = get_ingredient_status(recipe, user_inventory_map)
        insufficient_count = sum(1 for ing in ingredient_status if not ing['is_sufficient'])
        earliest_expiry = get_earliest_expiry_for_recipe(recipe, current_user.id)
        recs.append({
            'recipe': recipe, 
            'insufficient_count': insufficient_count,
            'ingredient_status': ingredient_status,
            'earliest_expiry': earliest_expiry
        })
    if sort == 'match':
        recs.sort(key=lambda r: r['insufficient_count'])
    elif sort == 'rating':
        recs.sort(key=lambda r: r['recipe'].average_rating, reverse=True)
    elif sort == 'expiry':
        recs.sort(key=lambda r: r['earliest_expiry'])
    elif sort == 'weighted':
        from datetime import date
        max_insufficient = max((r['insufficient_count'] for r in recs), default=1)
        max_expiry_days = max(((r['earliest_expiry'] - date.today()).days for r in recs), default=1)
        max_rating = max((r['recipe'].average_rating for r in recs), default=5.0)
        
        for r in recs:
            insufficient_score = r['insufficient_count'] / max_insufficient if max_insufficient > 0 else 0
            expiry_days = (r['earliest_expiry'] - date.today()).days
            expiry_score = expiry_days / max_expiry_days if max_expiry_days > 0 else 0
            rating_score = 1 - (r['recipe'].average_rating / max_rating) if max_rating > 0 else 0
            
            r['weighted_score'] = (0.5 * insufficient_score) + (0.3 * expiry_score) + (0.2 * rating_score)
        
        recs.sort(key=lambda r: r['weighted_score'])
    elif sort == 'all':
        recs.sort(key=lambda r: r['recipe'].name.lower())
    return render_template('recipes/recommend.html', recipes=recs, sort=sort)

@bp.route('/<int:recipe_id>')
@login_required
def detail(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    user_inventory_map = get_user_inventory_map(current_user.id)
    ingredient_status = get_ingredient_status(recipe, user_inventory_map)
    return render_template('recipes/detail.html', recipe=recipe, ingredient_status=ingredient_status)


@bp.route('/<int:recipe_id>/cook', methods=['POST'])
@login_required
def cook(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    user_id = current_user.id
    mode = request.args.get('add_to_list', 'none')

    shopping_list = None
    if mode in ('replace', 'missing'):
        list_name = recipe.name
        shopping_list = ShoppingList.query.filter_by(user_id=user_id, name=list_name).first()
        if not shopping_list:
            shopping_list = ShoppingList(user_id=user_id, name=list_name)
            db.session.add(shopping_list)
            db.session.flush()

    from sqlalchemy import asc
    added_items = []
    had_all = True
    for ri in recipe.ingredients:
        ing_unit_value = ri.ingredient.unit.value if hasattr(ri.ingredient.unit, 'value') else ri.ingredient.unit
        converted_needed = convert_recipe_to_ingredient_unit(ri.quantity or 0, ri.unit, ing_unit_value)
        needed = converted_needed if converted_needed is not None else (ri.quantity or 0)
        if needed <= 0:
            continue

        inv_items = (
            UserInventory.query
            .filter_by(user_id=user_id, ingredient_id=ri.ingredient_id)
            .order_by(asc(UserInventory.expiry_date))
            .all()
        )

        remaining = needed
        for inv in inv_items:
            if remaining <= 0:
                break
            take = min(inv.quantity, remaining)
            inv.quantity -= take
            remaining -= take
            if inv.quantity <= 0:
                db.session.delete(inv)

        if remaining > 0:
            had_all = False
            if mode == 'missing' and shopping_list is not None:
                sli = ShoppingListItem.query.filter_by(shopping_list_id=shopping_list.id, ingredient_id=ri.ingredient_id).first()
                if sli:
                    sli.quantity += remaining
                else:
                    sli = ShoppingListItem(shopping_list_id=shopping_list.id, ingredient_id=ri.ingredient_id, quantity=remaining)
                    db.session.add(sli)
                added_items.append((ri.ingredient.name, remaining, ri.unit.value if hasattr(ri.unit, 'value') else ri.unit))
        else:
            if mode == 'replace' and shopping_list is not None and needed > 0:
                sli = ShoppingListItem.query.filter_by(shopping_list_id=shopping_list.id, ingredient_id=ri.ingredient_id).first()
                if sli:
                    sli.quantity += needed
                else:
                    sli = ShoppingListItem(shopping_list_id=shopping_list.id, ingredient_id=ri.ingredient_id, quantity=needed)
                    db.session.add(sli)
                added_items.append((ri.ingredient.name, needed, ri.unit.value if hasattr(ri.unit, 'value') else ri.unit))

    db.session.commit()

    if added_items:
        list_name = shopping_list.name if shopping_list else recipe.name
        if mode == 'replace':
            flash(f"Cooked '{recipe.name}'. Replacement items added to shopping list '{list_name}'.", 'info')
        elif mode == 'missing':
            flash(f"Cooked '{recipe.name}'. Missing items added to shopping list '{list_name}'.", 'info')
        else:
            flash(f"Cooked '{recipe.name}'. Inventory updated (no list additions).", 'success')
    else:
        flash(f"Cooked '{recipe.name}'. Inventory updated.", 'success')

    return redirect(url_for('recipes.detail', recipe_id=recipe.id))


@bp.route('/<int:recipe_id>/cook-check', methods=['GET'])
@login_required
def cook_check(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    user_inventory_map = get_user_inventory_map(current_user.id)
    status = get_ingredient_status(recipe, user_inventory_map)
    missing = [
        {
            'name': s['name'],
            'missing': s['missing'],
            'unit': s['unit_str']
        }
        for s in status if not s['is_sufficient']
    ]
    had_all = len(missing) == 0
    return {
        'had_all': had_all,
        'missing': missing
    }
