from flask import Blueprint

bp = Blueprint('inventory', __name__, url_prefix='/inventory')

@bp.route('/')
def index():
    return 'Inventory page'

@bp.route('/add')
def add():
    return 'Add ingredient'
