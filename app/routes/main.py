from flask import Blueprint, jsonify, request, current_app

from app.models.products import ProductDBModel, Product, UpdateProduct
from app.models.user import LoginPayload
from pydantic import ValidationError
from app import db
from bson import ObjectId
from app.decorators import token_required
from datetime import datetime, timedelta, timezone
import jwt

main_bp = Blueprint('main_bp', __name__)

@main_bp.route('/login', methods=['POST'])
def login():
    login_data = None
    try:
        raw_data = request.get_json()
        login_data = LoginPayload(**raw_data)
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400
    except Exception as e:
        jsonify({"error": "Erro durante a requisição"}), 500

    if login_data.username == "admin" or login_data.password == "admin":
        token = jwt.encode(
            {
                "user_id": login_data.username,
                "exp": datetime.now(timezone.utc) + timedelta(minutes=30)
            },
            current_app.config["SECRET_KEY"],
            algorithm="HS256"
        )
        return jsonify({"access_token": token}), 200
    else:
        return jsonify({"message": "Acesso não autorizado"}), 401

@main_bp.route('/products', methods=['GET'])
def get_products():
    products_cursor = db.products.find({})
    products_list = [ProductDBModel(**product).model_dump(by_alias=True, exclude_none=True) for product in products_cursor]

    return jsonify(products_list)

@main_bp.route('/products/<string:product_id>')
def get_product_by_id(product_id):
    try:
        oid = ObjectId(product_id)
    except Exception as e:
        return jsonify({"error": f"Erro ao transformar o {product_id} em ObjectId: {e}"}), 400

    product = db.products.find_one({'_id': oid})

    if product:
        product_model = ProductDBModel(**product).model_dump(by_alias=True, exclude_none=True)
        return jsonify(product_model)
    else:
        return jsonify({"error": f"Produto com o id {product_id} não encontrado"}), 404

@main_bp.route('/products/<string:product_id>', methods=['PUT'])
@token_required
def update_product(token, product_id):
    try:
        oid = ObjectId(product_id)
        update_data = UpdateProduct(**request.get_json())
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400
    update_result = db.products.update_one(
        {'_id': oid},
        {'$set': update_data.model_dump(exclude_unset=True)}
    )

    if update_result.matched_count == 0:
        return jsonify({"error": "Produto não encontrado"}), 404

    updated_product = db.products.find_one({'_id': oid})
    return jsonify(ProductDBModel(**updated_product).model_dump(by_alias=True, exclude_none=True))

@main_bp.route('/products/<string:product_id>', methods=['DELETE'])
@token_required
def delete_product(token, product_id):
    try:
        oid = ObjectId(product_id)
    except Exception as e:
        return jsonify({"error": "ID do produto inválido"}), 400
    result = db.products.delete_one({'_id': oid})

    if result.deleted_count == 0:
        return jsonify({"error": "Produto não encontrado"}), 404

    return "", 204

@main_bp.route('/products', methods=['POST'])
@token_required
def create_product(token):
    try:
        product = Product(**request.get_json())
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

    result = db.products.insert_one(product.model_dump())

    return jsonify({"message": f"Produto com o id {result.inserted_id}"}), 201


@main_bp.route('/sales/upload', methods=['POST'])
def upload_sales():
    return jsonify({"message": "Esta é a rota de upload do arquivo de vendas"})

@main_bp.route('/')
def index():
    return jsonify({"message": "Bem vindo ao StyleSync!"})


