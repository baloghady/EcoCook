from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, DecimalField, DateField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, NumberRange, Optional
from app.models import User


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(message='Email is required.'),
        Email(message='Please enter a valid email address.')
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message='Password is required.')
    ])
    submit = SubmitField('Login')


class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(message='Email is required.'),
        Email(message='Please enter a valid email address.')
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message='Password is required.'),
        Length(min=8, message='Password must be at least 8 characters long.')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(message='Please confirm your password.'),
        EqualTo('password', message='Passwords must match.')
    ])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered. Please login or use a different email.')


class IngredientForm(FlaskForm):
    name = StringField('Ingredient Name', validators=[
        DataRequired(message='Ingredient name is required.'),
        Length(min=2, max=100, message='Name must be between 2 and 100 characters.')
    ])
    quantity = DecimalField('Quantity', validators=[
        DataRequired(message='Quantity is required.'),
        NumberRange(min=0.01, message='Quantity must be greater than 0.')
    ])
    unit = SelectField('Unit', validators=[
        DataRequired(message='Unit is required.')
    ], choices=[
        ('g', 'Grams (g)'),
        ('kg', 'Kilograms (kg)'),
        ('ml', 'Milliliters (ml)'),
        ('L', 'Liters (L)'),
        ('pieces', 'Pieces'),
        ('tbsp', 'Tablespoon (tbsp)'),
        ('tsp', 'Teaspoon (tsp)'),
        ('cup', 'Cup')
    ])
    expiry_date = DateField('Expiry Date (Optional)', validators=[Optional()], format='%Y-%m-%d')
    submit = SubmitField('Add to Inventory')
