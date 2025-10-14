from app import create_app
from app.extensions import db

def init_database():
    app = create_app()

    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        print("Database tables created successfully!")

        print("\nCreated tables:")
        print("- User")
        print("- Ingredient")
        print("- ShoppingList")
        print("- ShoppingListItem")
        print("- CookingHistory")

if __name__ == '__main__':
    init_database()
