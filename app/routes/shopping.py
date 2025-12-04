from hmac import new
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app import db
from app.utils.unit_service import convert_quantity
from app.models import ShoppingList, ShoppingListItem, Ingredient, UnitEnum

bp = Blueprint('shopping', __name__, url_prefix='/shopping')
#főoldal, mindet megjelenítsük
@bp.route('/')
@login_required
def index():
    shopping_lists = (
        ShoppingList.query
        .filter_by(user_id=current_user.id)
        .order_by(ShoppingList.created_at.desc())
        .all()
        )
    return render_template('shopping/list.html', shopping_lists=shopping_lists)
#újlista
@bp.route('/create', methods=['POST'])
@login_required
def create_list():
    name = request.form.get('name')
    if not name:
        flash('List name is required.', 'error')
        return redirect(url_for('shopping.index'))

    new_list = ShoppingList(name=name, user_id=current_user.id)
    db.session.add(new_list)
    db.session.commit()
    flash(f'New shopping list {name} created!', 'success')
    return redirect(url_for('shopping.index'))

@bp.route('/<int:list_id>/delete', methods=['POST'])
@login_required
def delete_list(list_id):
    shopping_list = ShoppingList.query.filter_by(id=list_id, user_id=current_user.id).first_or_404()
    db.session.delete(shopping_list)
    db.session.commit()
    flash('Shopping list deleted', 'warning')
    return redirect(url_for('shopping.index'))

@bp.route('/<int:list_id>/add', methods=['POST'])
@login_required
def add_item(list_id):
    shopping_list = ShoppingList.query.filter_by(id=list_id, user_id=current_user.id).first_or_404()

    ingredient_name = request.form.get('ingredient_name')
    quantity = request.form.get('quantity', type=float)
    unit_str = request.form.get('unit')
    try:
        unit = UnitEnum(unit_str)
    except ValueError:
        flash('Invalid unit selected.', 'error')
        return redirect(url_for('shopping.index'))

    if not ingredient_name or not quantity or not unit:
        flash('All fields are required.', 'error')
        return redirect(url_for('shopping.index'))
    #csekkoljuk van é már íly hozzátevő
    ingredient = Ingredient.query.filter_by(name=ingredient_name.lower()).first()
    if not ingredient:
        ingredient = Ingredient(name=ingredient_name.lower(), unit=unit)
        db.session.add(ingredient)
        db.session.commit()

    # Normalize entered quantity to ingredient's canonical unit for consistency with inventory
    ing_unit_value = ingredient.unit.value if hasattr(ingredient.unit, 'value') else ingredient.unit
    final_qty = convert_quantity(quantity, unit_str, ing_unit_value) or quantity
    new_item = ShoppingListItem(
        shopping_list_id=shopping_list.id,
        ingredient_id=ingredient.id,
        quantity=final_qty,
        is_purchased = False
    )
    db.session.add(new_item)
    db.session.commit()
    flash(f'Added {ingredient_name} to {shopping_list.name}.', 'success')
    return redirect(url_for('shopping.index'))

@bp.route('/<int:list_id>/toggle/<int:ingredient_id>', methods=['POST'])
@login_required
def toggle_purchased(list_id, ingredient_id):
    """AJAX végpont – megjelöli vagy eltávolítja a vásárolt státuszt egy elemről."""
    item = (
        ShoppingListItem.query
        .filter_by(shopping_list_id=list_id, ingredient_id=ingredient_id)
        .join(ShoppingList)
        .filter(ShoppingList.user_id == current_user.id)
        .first_or_404()
    )

    item.is_purchased = not item.is_purchased
    db.session.commit()
    return jsonify({'success': True, 'purchased': item.is_purchased})


# Egy elem törlése
@bp.route('/<int:list_id>/delete_item/<int:ingredient_id>', methods=['POST'])
@login_required
def delete_item(list_id, ingredient_id):
    """Töröl egy adott hozzávalót a listából."""
    item = (
        ShoppingListItem.query
        .filter_by(shopping_list_id=list_id, ingredient_id=ingredient_id)
        .join(ShoppingList)
        .filter(ShoppingList.user_id == current_user.id)
        .first_or_404()
    )
    db.session.delete(item)
    db.session.commit()
    flash('Item deleted.', 'warning')
    return redirect(url_for('shopping.index'))