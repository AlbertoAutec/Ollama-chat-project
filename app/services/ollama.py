# Funzione per interagire con Ollama tramite HTTP locale


import requests
import json

def ask_ollama(model, prompt):
    """
    Invia il prompt al modello Ollama scelto e restituisce la risposta.
    Gestisce anche la risposta streaming (più JSON su righe separate).
    """
    try:
        url = f"http://localhost:11434/api/chat"
        payload = {
            "model": model,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
        resp = requests.post(url, json=payload, timeout=120, stream=True)
        resp.raise_for_status()
        risposta = ""
        for line in resp.iter_lines():
            if line:
                try:
                    data = json.loads(line.decode('utf-8'))
                    # Ollama stream: "message" o "response"
                    if "message" in data and isinstance(data["message"], dict):
                        risposta += data["message"].get("content", "")
                    elif "response" in data:
                        risposta += data["response"]
                except Exception:
                    continue
        return risposta.strip() if risposta else "Nessuna risposta"
    except Exception as e:
        return f"Errore Ollama: {str(e)}"
