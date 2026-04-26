from flask import Flask
from .routes.main import main_bp
from pymongo import MongoClient

db = None

def create_app():
    app = Flask(__name__)
    app.register_blueprint(main_bp)
    app.config.from_object('config.Config')
    global db

    try:
        client = MongoClient(app.config['MONGO_URI'])
        db = client.get_default_database()
    except Exception as e:
        print(f'Erro ao realizar a conexão com o banco de dados: {e}')
    return app
