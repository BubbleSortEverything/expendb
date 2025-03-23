from flask import Blueprint, jsonify, request
from app.models.users import User
from app.extensions import db
from flask_restx import Api, Resource, fields

user_bp = Blueprint('user_bp', __name__)
api = Api(user_bp, version='1.0', title='User API', description='API for managing users')

# Define the Swagger Model
user_model = api.model('User', {
    'id': fields.Integer(description='User ID', readonly=True),
    'username': fields.String(required=True, description='Username of the user'),
    'email': fields.String(required=True, description='Email of the user')
})

health_model = api.model('Health', {
    'status': fields.String(description='Service status'),
    'message': fields.String(description='Health check message')
})


# Health Check Endpoint
@api.route('/health')
class HealthCheck(Resource):
    @api.doc('health_check')
    @api.marshal_with(health_model)
    def get(self):
        """Health check endpoint"""
        return {"status": "ok", "message": "Users service is running"}, 200


# Get All Users and Create User Endpoints
@api.route('/users')
class UserList(Resource):

    @api.doc('get_users')
    @api.marshal_list_with(user_model)
    def get(self):
        """Get a list of all users"""
        users = User.query.all()
        return users, 200

    @api.doc('create_user')
    @api.expect(user_model)
    @api.response(201, 'User created successfully')
    @api.response(400, 'Validation error')
    def post(self):
        """Create a new user"""
        data = request.get_json()

        # Simple validation
        if not data.get('username') or not data.get('email'):
            return {'message': 'Missing username or email'}, 400

        # Create and add new user
        new_user = User(username=data['username'], email=data['email'])
        db.session.add(new_user)
        db.session.commit()

        return {
            'id': new_user.id,
            'username': new_user.username,
            'email': new_user.email
        }, 201


# Get a Single User by ID
@api.route('/users/<int:user_id>')
@api.param('user_id', 'The ID of the user')
class SingleUser(Resource):

    @api.doc('get_user')
    @api.marshal_with(user_model)
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get a single user by ID"""
        user = User.query.get(user_id)

        if not user:
            api.abort(404, f"User with ID {user_id} not found")

        return user, 200
