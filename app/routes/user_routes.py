from flask import Blueprint, jsonify, request
from app.models.users import User
from app.extensions import db
from app.schemas.user_schema import UserSchema

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok", "message": "Users service is running"}), 200

@user_bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{'id': u.id, 'username': u.username, 'email': u.email} for u in users])

@user_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    errors = UserSchema.validate(data)

    if errors:
        return jsonify(errors), 400

    new_user = User(username=data['username'], email=data['email'])
    db.session.add(new_user)
    db.session.commit()

    return UserSchema.jsonify(new_user), 201
