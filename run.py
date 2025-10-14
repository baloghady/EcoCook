import os
from app import create_app
from app.extensions import db
from app import models

app = create_app(os.getenv('FLASK_ENV') or 'default')

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': models.User,
        'Ingredient': models.Ingredient,
        'ShoppingList': models.ShoppingList,
        'ShoppingListItem': models.ShoppingListItem,
        'CookingHistory': models.CookingHistory
    }

if __name__ == '__main__':
    app.run()
