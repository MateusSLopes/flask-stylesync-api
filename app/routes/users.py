from flask import Blueprint, jsonify, request
from pydantic import ValidationError
from app.models.user import UserResponse, UserCreate
from app import db
from bson import ObjectId
from app.decorators import token_required
from pwdlib import PasswordHash

users_bp = Blueprint('users_bp', __name__)

@users_bp.route('/users', methods=['GET'])
@token_required
def get_users(token):
    users_cursor = db.users.find({}, {"password": 0})
    users = [UserResponse(**user).model_dump(by_alias=True, exclude_none=True) for user in users_cursor]
    return jsonify(users)

@users_bp.route('/users', methods=['POST'])
def create_user():
    try:
        user_data = UserCreate(**request.get_json())
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

    username_search = db.users.find_one({"username": user_data.username})

    if username_search:
        return jsonify({"error": "O nome de usuário já existe"}), 400

    password_hasher = PasswordHash.recommended()
    user_data.password = password_hasher.hash(user_data.password)

    user = db.users.insert_one(user_data.model_dump())
    return jsonify({"message": f"Usuário criado com o id {user.inserted_id}"}), 201

@users_bp.route('/users/<string:user_id>', methods=['DELETE'])
@token_required
def delete_user(token, user_id):
    try:
        user_id = ObjectId(user_id)
    except Exception as e:
        return jsonify({"error": "O ID do usuário é inválido"}), 400

    deleted_user = db.users.delete_one({'_id': user_id})

    if deleted_user.deleted_count == 0:
        return jsonify({"error": f"O usuário de ID = {str(user_id)} não foi encontrado"}), 404

    return "", 204
