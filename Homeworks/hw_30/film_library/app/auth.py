# ---- Import Statements ----
from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import User
from flask_jwt_extended import create_access_token


# ---- Define Blueprint ----
auth_bp = Blueprint('auth', __name__)


# ---- Endpoints ----
@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Handle user registration.

    This endpoint registers a new user by accepting a JSON payload with 'username' and 'password'.
    It ensures the username is unique and saves the user to the database.

    :return: A JSON response indicating success or an error message with appropriate HTTP status.
    :rtype: flask.Response
    """
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({"error": "username and password required"}), 400

    existing_user = User.query.filter_by(username=data['username']).first()
    if existing_user:
        return jsonify({"error": "user already exists"}), 400

    user = User(username=data['username'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "user created successfully"}), 201


# ---- Login Endpoint ----
@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Handle user login.

    This endpoint authenticates a user by accepting a JSON payload with 'username' and 'password'.
    If authentication succeeds, it generates a JWT access token for the user.

    :return: A JSON response with the access token or an error message with appropriate HTTP status.
    :rtype: flask.Response
    """
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({"error": "username and password required"}), 400

    user = User.query.filter_by(username=data['username']).first()
    if not user or not user.check_password(data['password']):
        return jsonify({"error": "invalid username or password"}), 401

    access_token = create_access_token(identity=str(user.id))
    return jsonify({"access_token": access_token}), 200
