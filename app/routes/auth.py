# Blueprint per autenticazione: registrazione e login
from flask import Blueprint, request, jsonify
from app import db
from app.models.user import User

import jwt, datetime, os, re
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity

# ...definizione blueprint e altre route...

# Inserisci la route dopo la definizione di auth_bp


# ...altre route...

from app import limiter

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['POST'])
@limiter.limit("5 per minute")
def register():
    """
    Registra un nuovo utente.
    ---
    tags:
      - Auth
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              username:
                type: string
              email:
                type: string
              password:
                type: string
    responses:
      201:
        description: Registrazione avvenuta
      400:
        description: Dati non validi
      409:
        description: Utente già esistente
    """
    """
    Registra un nuovo utente. Richiede username, email, password.
    """
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    # Validazione avanzata
    if not username or not email or not password:
        return jsonify({'msg': 'Dati mancanti'}), 400
    # Username: 3-32 caratteri, solo lettere/numeri/._-
    if not re.fullmatch(r"^[a-zA-Z0-9_.-]{3,32}$", username):
        return jsonify({'msg': 'Username non valido (3-32 caratteri, solo lettere, numeri, _ . -)'}), 400
    # Email: regex robusta
    if not re.fullmatch(r"^(?=.{6,254}$)([a-zA-Z0-9_.+-]+)@([a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)$", email):
        return jsonify({'msg': 'Email non valida'}), 400
    # Password: min 8, almeno 1 maiuscola, 1 minuscola, 1 numero, 1 simbolo
    if len(password) < 8:
        return jsonify({'msg': 'Password troppo corta (min 8 caratteri)'}), 400
    if not re.search(r"[A-Z]", password):
        return jsonify({'msg': 'Password deve contenere almeno una lettera maiuscola'}), 400
    if not re.search(r"[a-z]", password):
        return jsonify({'msg': 'Password deve contenere almeno una lettera minuscola'}), 400
    if not re.search(r"[0-9]", password):
        return jsonify({'msg': 'Password deve contenere almeno un numero'}), 400
    if not re.search(r"[!@#$%^&*()_+\-=\[\]{};':\",.<>/?]", password):
        return jsonify({'msg': 'Password deve contenere almeno un simbolo'}), 400
    if User.query.filter((User.username==username)|(User.email==email)).first():
        return jsonify({'msg': 'Utente già esistente'}), 409
    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'msg': 'Registrazione avvenuta'}), 201

@auth_bp.route('/login', methods=['POST'])
@limiter.limit("10 per minute")
def login():
    """
    Login utente.
    ---
    tags:
      - Auth
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              username:
                type: string
              password:
                type: string
    responses:
      200:
        description: JWT e refresh token
      401:
        description: Credenziali non valide
    """
    """
    Login utente. Restituisce JWT valido 1h e refresh token valido 7 giorni.
    """
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({'msg': 'Credenziali non valide'}), 401
    access_token = create_access_token(identity=str(user.id), expires_delta=datetime.timedelta(hours=1))
    refresh_token = create_refresh_token(identity=str(user.id), expires_delta=datetime.timedelta(days=7))
    return jsonify({'access_token': access_token, 'refresh_token': refresh_token}), 200



# Endpoint per refresh token
@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
@limiter.limit("10 per minute")
def refresh():
    """
    Refresh token JWT.
    ---
    tags:
      - Auth
    security:
      - bearerAuth: []
    responses:
      200:
        description: Nuovo access token
      401:
        description: Token non valido
    """
    """
    Restituisce un nuovo access token usando un refresh token valido.
    """
    user_id = get_jwt_identity()
    access_token = create_access_token(identity=user_id, expires_delta=datetime.timedelta(hours=1))
    return jsonify({'access_token': access_token}), 200


# ...esistenti...




# Route per elenco utenti registrati (protetta)
@auth_bp.route('/users', methods=['GET'])
@jwt_required()
def list_users():
    """
    Restituisce l'elenco degli username registrati (protetto, solo autenticati).
    """
    users = User.query.with_entities(User.username).all()
    usernames = [u[0] for u in users]
    return jsonify({'users': usernames}), 200
