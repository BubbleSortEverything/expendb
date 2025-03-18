from app.models.user import User
from app.extensions import db

def get_all_users():
    return User.query.all()

def create_user(username, email):
    new_user = User(username=username, email=email)
    db.session.add(new_user)
    db.session.commit()
