from datetime import datetime
from flask_login import UserMixin
from app.extensions import db
from enum import Enum

class UnitEnum(Enum):
    tbsp = "tbsp"
    ml = "ml"
    g = "g"
    piece = "piece"
    tsp = "tsp"
    head = "head"
    slices = "slices"
    pinch = "pinch"
    cloves = "cloves"
    kg = "kg"
    l = "l"

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    diet_id = db.Column(db.Integer, db.ForeignKey('dietary_stuff.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    shopping_lists = db.relationship('ShoppingList', backref='user', lazy=True, cascade='all, delete-orphan')
    cooking_history = db.relationship('CookingHistory', backref='user', lazy=True, cascade='all, delete-orphan')
    inventory_items = db.relationship('UserInventory', backref='user', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<User {self.email}>'


class DietaryStuff(db.Model):
    __tablename__ = 'dietary_stuff'
    id = db.Column(db.Integer, primary_key=True)
    diet_name = db.Column(db.String(50), unique=True, nullable=False)
    diet_description = db.Column(db.String(255))

    #connections (kapcsolatok)
    users = db.relationship('User',backref='diet', lazy=True)
    recipes = db.relationship('Recipe', backref='diet', lazy=True)

    def __repr__(self):
        return f'<DietaryStuff {self.diet_name}>'


class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    category = db.Column(db.String(50))
    unit = db.Column(db.Enum(UnitEnum), nullable=False)
    carbon_footprint = db.Column(db.Float)
    seasonality = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    shopping_list_items = db.relationship('ShoppingListItem', backref='ingredient', lazy=True)
    inventory_items = db.relationship('UserInventory', backref='ingredient', lazy=True)

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
    shopping_list_id = db.Column(db.Integer, db.ForeignKey('shopping_list.id'), primary_key=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'), primary_key=True)
    quantity = db.Column(db.Float, nullable=False)
    is_purchased = db.Column(db.Boolean, default=False)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<ShoppingListItem {self.ingredient_id} x{self.quantity}>'


class UserInventory(db.Model):
    """Tracks ingredients owned by users with quantities and expiry dates"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    expiry_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<UserInventory User:{self.user_id} Ingredient:{self.ingredient_id} Qty:{self.quantity}>'

    def unit(self):
        return self.ingredient.unit.value

    @property
    def days_to_expiry(self):
        from datetime import date
        if not self.expiry_date:
            return None
        return (self.expiry_date - date.today()).days



# --- Recipe Models ---

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    servings = db.Column(db.Integer, default=4)
    prep_time = db.Column(db.Integer)  # minutes
    cook_time = db.Column(db.Integer)  # minutes
    difficulty = db.Column(db.String(20))
    cuisine = db.Column(db.String(50))
    diet_id = db.Column(db.Integer, db.ForeignKey('dietary_stuff.id'))  # ['vegan', 'gluten-free', etc.]
    instructions = db.Column(db.JSON)  # List of instruction steps
    nutrition = db.Column(db.JSON)  # Nutrition info dict
    image_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Simple rating system
    rating_sum = db.Column(db.Integer, default=0)
    rating_count = db.Column(db.Integer, default=0)

    ingredients = db.relationship('RecipeIngredient', backref='recipe', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Recipe {self.name}>'

    @property
    def average_rating(self):
        if self.rating_count > 0:
            return round(self.rating_sum / self.rating_count, 2)
        return 0

    @property
    def total_time(self):
        return (self.prep_time or 0) + (self.cook_time or 0)


class RecipeIngredient(db.Model):
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), primary_key=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'), primary_key=True)
    quantity = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(20), nullable=False)
    is_optional = db.Column(db.Boolean, default=False)

    ingredient = db.relationship('Ingredient')

    def __repr__(self):
        return f'<RecipeIngredient Recipe:{self.recipe_id} Ingredient:{self.ingredient_id} Qty:{self.quantity}>'




# --- Update CookingHistory to reference Recipe ---
class CookingHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=True)
    quantity_used = db.Column(db.Float, nullable=False)
    cooking_date = db.Column(db.DateTime, default=datetime.utcnow)
    carbon_saved = db.Column(db.Float)
    notes = db.Column(db.Text)

    recipe = db.relationship('Recipe')

    def __repr__(self):
        return f'<CookingHistory User:{self.user_id} Recipe:{self.recipe_id}>'

