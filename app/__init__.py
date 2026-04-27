from flask import Flask
from pymongo import MongoClient

db = None

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    global db

    try:
        client = MongoClient(app.config['MONGO_URI'])
        db = client.get_default_database()
    except Exception as e:
        print(f'Erro ao realizar a conexão com o banco de dados: {e}')

    from .routes.auth import auth_bp
    from .routes.products import products_bp
    from .routes.sales import sales_bp
    from .routes.users import users_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(sales_bp)
    app.register_blueprint(users_bp)

    return app
