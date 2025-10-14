from run import app
from app.extensions import db, bcrypt
from app.models import User

with app.app_context():
    existing_user = User.query.filter_by(email='test@ecocook.com').first()

    if existing_user:
        print('Test user already exists!')
        print('Email: test@ecocook.com')
        print('Password: test123')
    else:
        password_hash = bcrypt.generate_password_hash('test123').decode('utf-8')
        test_user = User(
            email='test@ecocook.com',
            password_hash=password_hash,
            dietary_preferences=['vegetarian']
        )
        db.session.add(test_user)
        db.session.commit()
        print('Test user created successfully!')
        print('Email: test@ecocook.com')
        print('Password: test123')
