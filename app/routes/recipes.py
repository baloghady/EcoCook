from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from app.models import Recipe, RecipeIngredient, UserInventory

bp = Blueprint('recipes', __name__, url_prefix='/recipes')


@bp.route('/')
@login_required
def index():
    sort = request.args.get('sort', 'match')
    recipes = Recipe.query.all()
    user_ingredient_ids = get_user_inventory_ids(current_user.id)
    recs = []
    for recipe in recipes:
        missing_count = get_missing_count(recipe, user_ingredient_ids)
        recs.append({'recipe': recipe, 'missing_count': missing_count})
    # Sort by priority
    if sort == 'match':
        recs.sort(key=lambda r: r['missing_count'])
    elif sort == 'rating':
        recs.sort(key=lambda r: r['recipe'].average_rating, reverse=True)
    elif sort == 'expiry':
        # Placeholder: sort by missing_count for now
        recs.sort(key=lambda r: r['missing_count'])
    elif sort ==  'all':
        recs.sort(key=lambda r: r['recipe'].name.lower())
    return render_template('recipes/recommend.html', recipes=recs, sort=sort)


def get_user_inventory_ids(user_id):
    return set(i.ingredient_id for i in UserInventory.query.filter_by(user_id=user_id).all())

def get_missing_ingredients(recipe, user_ingredient_ids):
    missing = []
    for ri in recipe.ingredients:
        if ri.ingredient_id not in user_ingredient_ids:
            missing.append(ri.ingredient.name)
    return missing

def get_missing_count(recipe, user_ingredient_ids):
    return sum(1 for ri in recipe.ingredients if ri.ingredient_id not in user_ingredient_ids)

@bp.route('/',endpoint='recipes_home')
@login_required
def index():
    return recommend()

@bp.route('/recommend')
@login_required
def recommend():
    sort = request.args.get('sort', 'match')
    recipes = Recipe.query.all()
    user_ingredient_ids = get_user_inventory_ids(current_user.id)
    recs = []
    for recipe in recipes:
        missing_count = get_missing_count(recipe, user_ingredient_ids)
        missing_ingredients = get_missing_ingredients(recipe, user_ingredient_ids)
        recs.append({'recipe': recipe, 'missing_count': missing_count, 'missing_ingredients': missing_ingredients})
    # Sort by priority
    if sort == 'match':
        recs.sort(key=lambda r: r['missing_count'])
    elif sort == 'rating':
        recs.sort(key=lambda r: r['recipe'].average_rating, reverse=True)
    elif sort == 'expiry':
        recs.sort(key=lambda r: r['missing_count'])
    elif sort == 'all':
        recs.sort(key=lambda r: r['recipe'].name.lower())
    return render_template('recipes/recommend.html', recipes=recs, sort=sort)

@bp.route('/<int:recipe_id>')
@login_required
def detail(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    user_ingredient_ids = get_user_inventory_ids(current_user.id)
    missing_ingredients = get_missing_ingredients(recipe, user_ingredient_ids)
    return render_template('recipes/detail.html', recipe=recipe, missing_ingredients=missing_ingredients)
