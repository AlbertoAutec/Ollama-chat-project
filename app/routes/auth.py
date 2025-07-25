# Blueprint per autenticazione: registrazione e login
from flask import Blueprint, request, jsonify
from app import db
from app.models.user import User
import jwt, datetime, os
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Registra un nuovo utente. Richiede username, email, password.
    """
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    if not username or not email or not password:
        return jsonify({'msg': 'Dati mancanti'}), 400
    if User.query.filter((User.username==username)|(User.email==email)).first():
        return jsonify({'msg': 'Utente già esistente'}), 409
    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'msg': 'Registrazione avvenuta'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Login utente. Restituisce JWT valido 1h.
    """
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({'msg': 'Credenziali non valide'}), 401
    access_token = create_access_token(identity=user.id, expires_delta=datetime.timedelta(hours=1))
    return jsonify({'access_token': access_token}), 200
