# Blueprint per chat e cronologia
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.user import User
from app.models.message import Message
from app.services.ollama import ask_ollama

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/chat', methods=['POST'])
@jwt_required()
def chat():
    """
    Endpoint protetto: invia prompt a Ollama, salva e restituisce risposta.
    """
    data = request.get_json()
    model = data.get('model')
    prompt = data.get('prompt')
    if not model or not prompt:
        return jsonify({'msg': 'Model e prompt richiesti'}), 400
    user_id = get_jwt_identity()
    response = ask_ollama(model, prompt)
    # Salva messaggio
    msg = Message(user_id=user_id, prompt=prompt, response=response, model=model)
    db.session.add(msg)
    db.session.commit()
    return jsonify({'response': response}), 200

@chat_bp.route('/history', methods=['GET'])
@jwt_required()
def history():
    """
    Restituisce la cronologia chat dell'utente autenticato.
    """
    user_id = get_jwt_identity()
    messages = Message.query.filter_by(user_id=user_id).order_by(Message.timestamp.desc()).all()
    return jsonify([
        {
            'prompt': m.prompt,
            'response': m.response,
            'model': m.model,
            'timestamp': m.timestamp.isoformat()
        } for m in messages
    ]), 200
