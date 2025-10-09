from flask import Blueprint

bp = Blueprint('shopping', __name__, url_prefix='/shopping')

@bp.route('/')
def index():
    return 'Shopping lists'

@bp.route('/create')
def create():
    return 'Create shopping list'
