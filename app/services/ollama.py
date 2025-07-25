# Funzione per interagire con Ollama tramite HTTP locale
import requests

def ask_ollama(model, prompt):
    """
    Invia il prompt al modello Ollama scelto e restituisce la risposta.
    """
    try:
        # Esempio: Ollama API locale su http://localhost:11434/api/chat
        url = f"http://localhost:11434/api/chat"
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}]
        }
        resp = requests.post(url, json=payload, timeout=60)
        resp.raise_for_status()
        data = resp.json()
        # Adatta in base alla risposta reale di Ollama
        return data.get('message', 'Nessuna risposta')
    except Exception as e:
        return f"Errore Ollama: {str(e)}"
