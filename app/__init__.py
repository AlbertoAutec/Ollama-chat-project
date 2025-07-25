# Inizializza il package Flask e carica le configurazioni
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

# Carica variabili da .env
load_dotenv()

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    """
    Crea e configura l'app Flask.
    """
    app = Flask(__name__)
    # Configurazione da variabili d'ambiente
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

    db.init_app(app)
    jwt.init_app(app)

    # Importa e registra le blueprint delle route
    from app.routes.auth import auth_bp
    from app.routes.chat import chat_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(chat_bp)

    return app
