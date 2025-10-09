from flask import Blueprint

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login')
def login():
    return 'Login page'

@bp.route('/register')
def register():
    return 'Register page'

@bp.route('/logout')
def logout():
    return 'Logout'
