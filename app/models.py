from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    dietary_preferences = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    shopping_lists = db.relationship('ShoppingList', backref='user', lazy=True, cascade='all, delete-orphan')
    cooking_history = db.relationship('CookingHistory', backref='user', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<User {self.email}>'


class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    category = db.Column(db.String(50))
    unit = db.Column(db.String(20), nullable=False)
    carbon_footprint = db.Column(db.Float)
    seasonality = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    shopping_list_items = db.relationship('ShoppingListItem', backref='ingredient', lazy=True)
    cooking_history_items = db.relationship('CookingHistory', backref='ingredient', lazy=True)

    def __repr__(self):
        return f'<Ingredient {self.name}>'


class ShoppingList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_completed = db.Column(db.Boolean, default=False)

    items = db.relationship('ShoppingListItem', backref='shopping_list', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<ShoppingList {self.name} (User: {self.user_id})>'


class ShoppingListItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    shopping_list_id = db.Column(db.Integer, db.ForeignKey('shopping_list.id'), nullable=False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    is_purchased = db.Column(db.Boolean, default=False)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<ShoppingListItem {self.ingredient_id} x{self.quantity}>'


class CookingHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'), nullable=False)
    recipe_name = db.Column(db.String(200))
    quantity_used = db.Column(db.Float, nullable=False)
    cooking_date = db.Column(db.DateTime, default=datetime.utcnow)
    carbon_saved = db.Column(db.Float)
    notes = db.Column(db.Text)

    def __repr__(self):
        return f'<CookingHistory User:{self.user_id} Recipe:{self.recipe_name}>'

