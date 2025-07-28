# Inizializza il package Flask e carica le configurazioni
from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv
import os

# Carica variabili da .env
load_dotenv()


db = SQLAlchemy()
jwt = JWTManager()
limiter = Limiter(key_func=get_remote_address)

def create_app():
    """
    Crea e configura l'app Flask.
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    template_dir = os.path.join(base_dir, "templates_ollama")
    static_dir = os.path.join(base_dir, "static_ollama")
    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
    # Swagger/OpenAPI (Flasgger)
    from flasgger import Swagger
    Swagger(app)
    # Rate limiting globale
    limiter.init_app(app)
    # Configurazione da variabili d'ambiente
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')


    db.init_app(app)
    jwt.init_app(app)

    # Abilita CORS globale
    from flask_cors import CORS
    CORS(app)



    # Logging avanzato: su file e console, livelli INFO e ERROR
    import logging
    from logging.handlers import RotatingFileHandler
    log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s %(message)s')
    # File log (max 1MB, 5 backup)
    file_handler = RotatingFileHandler('app.log', maxBytes=1_000_000, backupCount=5)
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(logging.INFO)
    # Console log
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    console_handler.setLevel(logging.INFO)
    # Root logger
    logging.basicConfig(level=logging.INFO, handlers=[file_handler, console_handler])

    # Importa e registra le blueprint delle route
    from app.routes.auth import auth_bp
    from app.routes.chat import chat_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(chat_bp)

    # Handler globale per errori 500
    @app.errorhandler(500)
    def handle_500(e):
        logging.exception("Errore interno del server")
        return {'msg': 'Errore interno del server'}, 500

    return app
