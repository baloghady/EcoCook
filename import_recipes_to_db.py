import json
from app import create_app
from app.extensions import db
from app.models import Recipe, Ingredient, RecipeIngredient

app = create_app()

with app.app_context():
    with open('data/recipes.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    recipes = data.get('recipes', [])
    for r in recipes:
        # Create or get ingredients
        ingredient_objs = []
        for ing in r['ingredients']:
            name = ing['name'].strip().lower()
            unit = ing.get('unit', 'pieces')
            ingredient = Ingredient.query.filter(Ingredient.name.ilike(name)).first()
            if not ingredient:
                ingredient = Ingredient(name=name, unit=unit)
                db.session.add(ingredient)
                db.session.flush()  # get id
            ingredient_objs.append((ingredient, ing['quantity'], unit))
        # Create recipe
        recipe = Recipe(
            name=r['name'],
            description=r.get('description'),
            servings=r.get('servings', 1),
            prep_time=r.get('prep_time'),
            cook_time=r.get('cook_time'),
            difficulty=r.get('difficulty'),
            cuisine=r.get('cuisine'),
            dietary_tags=r.get('dietary_tags'),
            instructions=r.get('instructions'),
            nutrition=r.get('nutrition'),
            image_url=r.get('image_url'),
        )
        db.session.add(recipe)
        db.session.flush()  # get id
        # Link ingredients
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
