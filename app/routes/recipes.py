from flask import Blueprint

bp = Blueprint('recipes', __name__, url_prefix='/recipes')

@bp.route('/')
def index():
    return 'Recipes page'

@bp.route('/<recipe_id>')
def detail(recipe_id):
    return f'Recipe detail: {recipe_id}'
