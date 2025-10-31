from app import create_app, db
from app.models import Recipe, RecipeIngredient, Ingredient, DietaryStuff, UnitEnum
from datetime import datetime

app = create_app()

# --- alap diéták ---
BASE_DIETS = {
    "Vegan": "No animal products.",
    "Vegetarian": "No meat, may include dairy and eggs.",
    "Gluten-Free": "Free from gluten-containing ingredients.",
    "High-Protein": "Rich in protein sources.",
    "Dairy-Free": "No milk or dairy products."
}

# --- receptek ---
RECIPES = [
    {
        "name": "Vegetable Stir Fry",
        "description": "Quick and healthy stir-fry with mixed vegetables.",
        "servings": 4,
        "prep_time": 15,
        "cook_time": 10,
        "difficulty": "easy",
        "cuisine": "Asian",
        "diet": "Vegan",
        "instructions": [
            "Heat oil in a wok.",
            "Add garlic and vegetables.",
            "Stir-fry for 5-7 minutes.",
            "Add soy sauce and serve hot."
        ],
        "nutrition": {"calories": 120, "protein": 5, "carbs": 18, "fat": 4},
        "ingredients": [
            ("Broccoli", 200, "g"),
            ("Carrot", 2, "piece"),
            ("Soy Sauce", 3, "tbsp"),
            ("Garlic", 2, "cloves")
        ]
    },
    {
        "name": "Spaghetti Bolognese",
        "description": "Classic Italian pasta with a rich tomato-meat sauce.",
        "servings": 4,
        "prep_time": 20,
        "cook_time": 40,
        "difficulty": "medium",
        "cuisine": "Italian",
        "diet": "High-Protein",
        "instructions": [
            "Cook spaghetti according to package instructions.",
            "Sauté onion and garlic, add minced beef.",
            "Add tomato sauce and simmer for 30 minutes."
        ],
        "nutrition": {"calories": 550, "protein": 25, "carbs": 60, "fat": 20},
        "ingredients": [
            ("Spaghetti", 300, "g"),
            ("Minced Beef", 400, "g"),
            ("Tomato Sauce", 500, "ml"),
            ("Onion", 1, "piece"),
            ("Garlic", 2, "cloves")
        ]
    },
    {
        "name": "Avocado Toast",
        "description": "Simple and nutritious breakfast toast.",
        "servings": 2,
        "prep_time": 5,
        "cook_time": 0,
        "difficulty": "easy",
        "cuisine": "American",
        "diet": "Vegan",
        "instructions": [
            "Toast the bread slices.",
            "Mash avocado with lemon juice, salt, and pepper.",
            "Spread on toast and serve."
        ],
        "nutrition": {"calories": 250, "protein": 6, "carbs": 20, "fat": 15},
        "ingredients": [
            ("Avocado", 1, "piece"),
            ("Bread", 2, "slices"),
            ("Lemon", 0.5, "piece"),
            ("Salt", 1, "pinch"),
            ("Pepper", 1, "pinch")
        ]
    },
    # ... (a többi recept változatlan marad)
]


def seed_recipes():
    with app.app_context():
        # --- diéták ---
        if DietaryStuff.query.count() == 0:
            for name, desc in BASE_DIETS.items():
                db.session.add(DietaryStuff(diet_name=name, diet_description=desc))
            db.session.commit()
            print("🌿 Seeded DietaryStuff table.")

        # --- receptek ---
        if Recipe.query.count() > 0:
            print("ℹ️ Recipes already exist, skipping seeding.")
            return

        for data in RECIPES:
            diet = DietaryStuff.query.filter_by(diet_name=data["diet"]).first()

            recipe = Recipe(
                name=data["name"],
                description=data["description"],
                servings=data["servings"],
                prep_time=data["prep_time"],
                cook_time=data["cook_time"],
                difficulty=data["difficulty"],
                cuisine=data["cuisine"],
                diet_id=diet.id if diet else None,
                instructions=data["instructions"],
                nutrition=data["nutrition"],
                created_at=datetime.utcnow()
            )
            db.session.add(recipe)
            db.session.flush()

            # --- hozzávalók ---
            for (name, qty, unit_str) in data["ingredients"]:
                # 1️⃣ konvertáljuk string → UnitEnum
                try:
                    unit_enum = UnitEnum(unit_str.lower())
                except ValueError:
                    print(f"⚠️ Warning: '{unit_str}' not in UnitEnum. Skipping ingredient {name}.")
                    continue

                ingredient = Ingredient.query.filter_by(name=name).first()
                if not ingredient:
                    ingredient = Ingredient(name=name, unit=unit_enum)
                    db.session.add(ingredient)
                    db.session.flush()

                db.session.add(RecipeIngredient(
                    recipe_id=recipe.id,
                    ingredient_id=ingredient.id,
                    quantity=qty,
                    unit=unit_enum.value
                ))

        db.session.commit()
        print("✅ Seeded recipes successfully.")


if __name__ == "__main__":
    seed_recipes()


        #KEDVES FEJLESZTŐTÁRSAIM!!!!! EZT NEKTEK HAGYTAM BENT, HA LEFUTTATTÁTOK BASH-EL AKKOR KI LEHET TÖRÖLNNI. 
        #ANNYIT CSINÁL HOGY AZ ADATBÁZIS [DIETARYSTUFF] TÁBLÁJÁT FELTÖLTI PÁR ALAPADATTAL
        #GG EZ