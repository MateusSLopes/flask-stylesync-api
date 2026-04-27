from flask import Blueprint, jsonify, request
from pydantic import ValidationError
from app.models.sale import Sale
from app import db
from app.decorators import token_required
import csv
import io

sales_bp = Blueprint('sales_bp', __name__)

@sales_bp.route('/sales/upload', methods=['POST'])
@token_required
def upload_sales(token):
    if 'file' not in request.files:
        return jsonify({"error": "Nenhum arquivo foi enviado!"}), 400
    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "Nenhum arquivo foi enviado!"}), 400

    if file and file.filename.endswith('.csv'):
        csv_stream = io.StringIO(file.stream.read().decode('UTF-8'), newline=None)
        csv_reader = csv.DictReader(csv_stream)

        sales_to_insert = []
        error = []

        for row_num, row in enumerate(csv_reader, 1):
            try:
                sale_data = Sale(**row)
                sales_to_insert.append(sale_data.model_dump())
            except ValidationError as e:
                error.append(f'Linha {row_num} com dados inválidos')
            except Exception as e:
                error.append(f'Linha {row_num} com erro inesperado nos dados')

        if sales_to_insert:
            try:
                db.sales.insert_many(sales_to_insert)
            except Exception as e:
                return jsonify({"error": str(e)}), 400

        return jsonify({
            "message": "Upload realizado com sucesso",
            "sales": sales_to_insert,
            "errors": error
        }), 200
