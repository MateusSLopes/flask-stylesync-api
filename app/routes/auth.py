from flask import Blueprint, jsonify, request, current_app
from pydantic import ValidationError
from app.models.user import LoginPayload
from app import db
from datetime import datetime, timedelta, timezone
import jwt
from pwdlib import PasswordHash

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    login_data = None
    try:
        raw_data = request.get_json()
        login_data = LoginPayload(**raw_data)
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400
    except Exception as e:
        return jsonify({"error": "Erro durante a requisição"}), 500

    user = db.users.find_one({"username": login_data.username})

    password_hasher = PasswordHash.recommended()

    if not user or not password_hasher.verify(login_data.password, user["password"]):
        return jsonify({"error": "As credenciais de acesso são inválidas!"}), 401

    token = jwt.encode(
        {
            "user_id": login_data.username,
            "exp": datetime.now(timezone.utc) + timedelta(minutes=30)
        },
        current_app.config["SECRET_KEY"],
        algorithm="HS256"
    )

    return jsonify({"access_token": token}), 200
