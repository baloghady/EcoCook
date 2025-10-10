from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from config import config
from app.models import User

# Globális objektumok
db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()

# Flask app factory
def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Inicializálás
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)


    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'

    from app.routes import auth, inventory, recipes, shopping
    app.register_blueprint(auth.bp)
    app.register_blueprint(inventory.bp)
    app.register_blueprint(recipes.bp)
    app.register_blueprint(shopping.bp)

    return app


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
