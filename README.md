# 🌱 EcoCook - Sustainable Cooking Assistant

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Build Status](https://img.shields.io/badge/build-in_progess-yellow.svg)]()

> A web application for environmentally conscious and economical cooking that helps reduce food waste through intelligent ingredient management and personalized recipe recommendations.

---

## 📖 Table of Contents

- [About](#-about)
- [Features](#-features)
- [Technologies](#-technologies)
- [Usage Guide](#-usage-guide)
- [Structure](#-structure)
- [Roadmap](#-roadmap)
- [License](#-license)
- [Project Stats](#-project-stats)

---

## 🎯 About

**EcoCook** is a sustainable cooking assistant designed to help users:
- **Reduce food waste** by tracking ingredient expiry dates
- **Save money** through intelligent meal planning
- **Cook sustainably** with personalized recipe recommendations based on available ingredients
- **Shop smarter** with automatically generated shopping lists

The application combines inventory management, recipe suggestion algorithms, and waste reduction analytics to promote environmentally conscious cooking habits.

---

## ✨ Features

### Core Functionality
- 🥬 **Ingredient Inventory Management** - Track all your ingredients with quantities, units, and expiry dates
- 🍳 **Smart Recipe Recommendations** - Get personalized recipe suggestions based on what you have
- 🥗 **Dietary Preference Filtering** - Support for vegan, vegetarian, gluten-free, dairy-free, and more
- 📊 **Automatic Inventory Updates** - Ingredients are automatically deducted when you cook a recipe
- 🛒 **Smart Shopping Lists** - Generate optimized shopping lists for missing ingredients
- ⚖️ **Serving Size Adjustment** - Dynamically scale recipes for any number of servings
- 📅 **Expiry Date Alerts** - Get notified about ingredients that are about to expire
- 📈 **Waste Reduction Analytics** - Track your environmental impact and money saved

### Advanced Features
- 🔍 **Intelligent Search** - Find recipes by name, ingredients, dietary tags, or cooking time
- ⭐ **Recipe Ratings** - Rate and review recipes you've cooked
- 📜 **Cooking History** - Keep track of all recipes you've made
- 🎯 **Personalized Dashboard** - Overview of your inventory, recommended recipes, and statistics
- 📱 **Mobile Responsive** - Works seamlessly on desktop, tablet, and mobile devices

---

## 🛠️ Technologies

### Backend
- **[Python 3.9+](https://www.python.org/)** - Programming language
- **[Flask 3.0](https://flask.palletsprojects.com/)** - Web framework
- **[Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/)** - Database ORM
- **[Flask-Login](https://flask-login.readthedocs.io/)** - User authentication
- **[Flask-WTF](https://flask-wtf.readthedocs.io/)** - Form handling and validation
- **[Flask-Bcrypt](https://flask-bcrypt.readthedocs.io/)** - Password hashing
- **[SQLite](https://www.sqlite.org/)** - Database

### Frontend
- **HTML5** - Markup
- **CSS3** - Styling
- **JavaScript (Vanilla)** - Client-side interactivity

### Data & Algorithms
- **JSON** - Recipe data storage

### Development Tools
- **Git** - Version control
- **pytest** - Testing framework
- **pip** - Package management
- **venv** - Virtual environment

---

## 📘 Usage Guide

### 1. Managing Your Inventory

**Add Ingredients:**
1. Navigate to "My Inventory" from the navigation menu
2. Click "Add Ingredient" button
3. Fill in the details:
   - Name (e.g., "Tomatoes")
   - Quantity (e.g., 5)
   - Unit (e.g., "pieces")
   - Category (e.g., "Vegetables")
   - Expiry Date (optional)
4. Click "Save"

**Edit or Delete:**
- Click the edit icon to modify ingredient details
- Click the delete icon to remove an ingredient

### 2. Finding Recipes

**Browse All Recipes:**
- Go to "Recipes" in the navigation menu
- Browse through available recipes

**Search and Filter:**
- Use the search bar to find recipes by name
- Apply filters:
  - Difficulty level
  - Cooking time
  - Dietary preferences
  - Cuisine type

**View Recipe Details:**
- Click on any recipe card to see full details
- View ingredients, instructions, and nutrition info
- Adjust serving size with the slider

### 3. Getting Recommendations

**Personalized Suggestions:**
- Go to your Dashboard or "Recommended for You" section
- EcoCook analyzes your inventory and suggests recipes
- Recipes are prioritized based on:
  - How many ingredients you already have
  - Ingredients that are expiring soon
  - Your dietary preferences

### 4. Cooking a Recipe

1. Open a recipe detail page
2. Review the ingredients and instructions
3. Click "Cook This Recipe"
4. Confirm the number of servings
5. The app automatically:
   - Deducts used ingredients from your inventory
   - Records the recipe in your cooking history
   - Updates waste reduction statistics

### 5. Creating Shopping Lists

**Automatic Generation:**
1. Select one or more recipes you want to cook
2. Click "Generate Shopping List"
3. The app calculates missing ingredients
4. Review and edit the list if needed
5. Save the shopping list

**Manual Creation:**
1. Go to "Shopping Lists"
2. Click "Create New List"
3. Add items manually
4. Check off items as you shop

### 6. Tracking Your Impact

**View Analytics:**
- Navigate to "Analytics" or your Dashboard
- See metrics like:
  - Ingredients saved from expiring
  - Money saved estimate
  - Environmental impact (CO2, water saved)
  - Most cooked recipes
  - Waste reduction trends over time

---

## 🏗️ Structure

### Project structure
```
ecocook/
│
├── app/
│   ├── __init__.py              # Flask app factory
│   ├── models.py                # SQLAlchemy models
│   ├── forms.py                 # WTForms forms
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py              # Login/Register routes
│   │   ├── inventory.py         # Inventory management
│   │   ├── recipes.py           # Recipe search/display
│   │   └── shopping.py          # Shopping list
│   ├── utils/
│   │   ├── recipe_matcher.py    # Recipe matching algorithm
│   │   ├── inventory_updater.py # Inventory update logic
│   │   └── unit_converter.py    # Unit conversion
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css
│   │   ├── js/
│   │   │   └── main.js
│   │   └── images/
│   └── templates/
│       ├── base.html            # Base template
│       ├── auth/
│       │   ├── login.html
│       │   └── register.html
│       ├── inventory/
│       │   ├── index.html
│       │   └── add.html
│       ├── recipes/
│       │   ├── search.html
│       │   └── detail.html
│       └── shopping/
│           └── list.html
│
├── data/
│   └── recipes.json             # Static recipe database
│
├── tests/
│   ├── test_auth.py
│   ├── test_inventory.py
│   └── test_recipes.py
│
├── migrations/                   # Flask-Migrate files
├── config.py                    # Configuration
├── requirements.txt             # Python dependencies
├── run.py                       # Application entry point
└── README.md
```

### Database schema
```
# models.py structure

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    dietary_preferences = db.Column(db.JSON)  # ['vegan', 'gluten-free']
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(20), nullable=False)
    expiry_date = db.Column(db.Date, nullable=True)
    category = db.Column(db.String(50))
    added_at = db.Column(db.DateTime, default=datetime.utcnow)

class ShoppingList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='active')

class ShoppingListItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    list_id = db.Column(db.Integer, db.ForeignKey('shopping_list.id'))
    ingredient_name = db.Column(db.String(100))
    quantity = db.Column(db.Float)
    unit = db.Column(db.String(20))
    checked = db.Column(db.Boolean, default=False)

class CookingHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    recipe_id = db.Column(db.String(50))  # ID from recipes.json
    date = db.Column(db.DateTime, default=datetime.utcnow)
    servings_made = db.Column(db.Integer)
```

### recipes.json structure
```
{
  "recipes": [
    {
      "id": "recipe_001",
      "name": "Vegetable Stir Fry",
      "description": "Quick and healthy stir fry",
      "servings": 4,
      "prep_time": 15,
      "cook_time": 10,
      "difficulty": "easy",
      "cuisine": "Asian",
      "dietary_tags": ["vegan", "gluten-free"],
      "ingredients": [
        {"name": "broccoli", "quantity": 200, "unit": "g"},
        {"name": "carrot", "quantity": 2, "unit": "pieces"},
        {"name": "soy sauce", "quantity": 3, "unit": "tbsp"},
        {"name": "garlic", "quantity": 3, "unit": "cloves"}
      ],
      "instructions": [
        "Heat oil in a large pan or wok",
        "Add garlic and stir for 30 seconds",
        "Add vegetables and stir-fry for 5-7 minutes",
        "Add soy sauce and cook for 2 more minutes"
      ],
      "nutrition": {
        "calories": 120,
        "protein": 5,
        "carbs": 18,
        "fat": 4
      },
      "image_url": "stir_fry.jpg"
    }
  ]
}
```

---

## 🗺️ Roadmap

### 🔄 Version 1.0 - In Progress
- [ ] User authentication
- [ ] Ingredient inventory management
- [ ] Recipe browsing and search
- [ ] Basic recipe recommendations
- [ ] Shopping list creation
- [ ] Automatic inventory updates

### 📋 Version 2.0 - Planned
- [ ] Improved recommendation algorithm
- [ ] Waste reduction analytics dashboard
- [ ] Recipe rating and reviews
- [ ] Cooking history tracking
- [ ] Expiry date notifications

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

### Built With ❤️ and Python

---

## 📊 Project Stats

![GitHub stars](https://img.shields.io/github/stars/baloghady/ecocook?style=social)
![GitHub forks](https://img.shields.io/github/forks/baloghady/ecocook?style=social)
![GitHub issues](https://img.shields.io/github/issues/baloghady/ecocook)
![GitHub pull requests](https://img.shields.io/github/issues-pr/baloghady/ecocook)

---

**🍳 Happy Cooking! Let's reduce food waste together! 🌍**
