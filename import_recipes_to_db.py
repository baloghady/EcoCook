import json
import random
from app import create_app
from app.extensions import db
from app.models import Recipe, Ingredient, RecipeIngredient, UnitEnum

app = create_app()

def map_unit_to_enum(unit_str):
    """Map unit string to UnitEnum, handling common variations"""
    unit_map = {
        'pieces': UnitEnum.piece,
        'piece': UnitEnum.piece,
        'cup': UnitEnum.ml,
        'cups': UnitEnum.ml,
        'tbsp': UnitEnum.tbsp,
        'tsp': UnitEnum.tsp,
        'g': UnitEnum.g,
        'ml': UnitEnum.ml,
        'kg': UnitEnum.kg,
        'l': UnitEnum.l,
        'cloves': UnitEnum.cloves,
        'head': UnitEnum.head,
        'slices': UnitEnum.slices,
        'pinch': UnitEnum.pinch
    }
    return unit_map.get(unit_str.lower(), UnitEnum.piece)

def generate_ratings():
    """Generate realistic rating data for a recipe"""
    rating_type = random.choices(['high', 'medium', 'low'], weights=[70, 20, 10])[0]
    
    if rating_type == 'high':
        avg_rating = random.uniform(4.0, 5.0)
        rating_count = random.randint(15, 100)
    elif rating_type == 'medium':
        avg_rating = random.uniform(3.0, 3.9)
        rating_count = random.randint(8, 40)
    else:
        avg_rating = random.uniform(1.5, 2.9)
        rating_count = random.randint(3, 15)
    
    rating_sum = int(avg_rating * rating_count)
    return rating_sum, rating_count

with app.app_context():
    with open('data/recipes.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    recipes = data.get('recipes', [])
    for r in recipes:
        ingredient_objs = []
        for ing in r['ingredients']:
            name = ing['name'].strip().lower()
            unit_str = ing.get('unit', 'piece')
            unit_enum = map_unit_to_enum(unit_str)
            
            ingredient = Ingredient.query.filter(Ingredient.name.ilike(name)).first()
            if not ingredient:
                ingredient = Ingredient(name=name, unit=unit_enum)
                db.session.add(ingredient)
                db.session.flush()
            ingredient_objs.append((ingredient, ing['quantity'], unit_str))
        
        rating_sum, rating_count = generate_ratings()
        
        recipe = Recipe(
            name=r['name'],
            description=r.get('description'),
            servings=r.get('servings', 1),
            prep_time=r.get('prep_time'),
            cook_time=r.get('cook_time'),
            difficulty=r.get('difficulty'),
            cuisine=r.get('cuisine'),
            instructions=r.get('instructions'),
            nutrition=r.get('nutrition'),
            image_url=r.get('image_url'),
            rating_sum=rating_sum,
            rating_count=rating_count,
        )
        db.session.add(recipe)
        db.session.flush()
        for ingredient, qty, unit in ingredient_objs:
            ri = RecipeIngredient(
                recipe_id=recipe.id,
                ingredient_id=ingredient.id,
                quantity=qty,
                unit=unit,
            )
            db.session.add(ri)
    db.session.commit()
    print(f"Imported {len(recipes)} recipes.")
