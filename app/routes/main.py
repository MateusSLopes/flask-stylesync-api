from flask import Blueprint, jsonify, request
from app.models.user import LoginPayload
from pydantic import ValidationError

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
        return jsonify({"message": "Bem vindo ao StyleSync!"}), 200
    else:
        return jsonify({"message": "Acesso não autorizado"}), 403

@main_bp.route('/products')
def get_products():
    return jsonify({"message": "Esta é a rota de listagem dos produtos"})

@main_bp.route('/products/<int:product_id>')
def get_product_by_id(product_id):
    return jsonify({"message": f"Esta é a rota de visualização detalhada do produto de id {product_id}"})

@main_bp.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    return jsonify({"message": f"Esta é a rota de atualização do produto de id {product_id}"})

@main_bp.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    return jsonify({"message": f"Esta é a rota de exclusão do produto de id {product_id}"})

@main_bp.route('/products', methods=['POST'])
def create_product():
    return jsonify({"message": "Esta é a rota de criação de produtos"})

@main_bp.route('/sales/upload', methods=['POST'])
def upload_sales():
    return jsonify({"message": "Esta é a rota de upload do arquivo de vendas"})

@main_bp.route('/')
def index():
    return jsonify({"message": "Bem vindo ao StyleSync!"})


