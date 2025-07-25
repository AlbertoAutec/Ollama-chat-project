# Ollama Chat API (Flask + SQL Server)

API RESTful per chat AI con autenticazione JWT, database SQL Server e scelta modello Ollama.

## Funzionalità principali
- **Registrazione e login utenti** (JWT)
- **Endpoint protetti** per chat e cronologia
- **Scelta modello Ollama** per ogni messaggio
- **Salvataggio messaggi** e cronologia su SQL Server
- **Struttura MVC** con Flask, SQLAlchemy, JWT, pyodbc

## Struttura progetto
```
Ollama-chat/
├── app/
│   ├── __init__.py           # Inizializza Flask, DB, JWT, blueprint
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py           # Modello utente
│   │   └── message.py        # Modello messaggio
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py           # Registrazione e login
│   │   └── chat.py           # Chat e cronologia
│   └── services/
│       ├── __init__.py
│       └── ollama.py         # Chiamate HTTP a Ollama
├── main.py                   # Entry point Flask
├── requirements.txt          # Dipendenze
├── Dockerfile                # Esempio container
├── .env.example              # Esempio variabili ambiente
└── README.md                 # (questo file)
```

## Setup rapido
1. **Copia `.env.example` in `.env`** e inserisci le tue credenziali DB e secret JWT.
2. **Installa le dipendenze:**
   ```sh
   pip install -r requirements.txt
   ```
3. **Crea il database SQL Server** e aggiorna la stringa `DATABASE_URL` nel `.env`.
4. **Avvia Ollama** in locale (es: `ollama serve` su http://localhost:11434).
5. **Avvia l'app:**
   ```sh
   python main.py
   ```

## Esempio file `.env`
```
DATABASE_URL=mssql+pyodbc://USERNAME:PASSWORD@SERVER/DATABASE?driver=ODBC+Driver+17+for+SQL+Server
JWT_SECRET_KEY=super-secret-key
```

## Endpoints principali

### Registrazione
`POST /auth/register`
```json
{
  "username": "alberto",
  "email": "alberto@email.com",
  "password": "password"
}
```

### Login
`POST /auth/login`
```json
{
  "username": "alberto",
  "password": "password"
}
Risposta: { "access_token": "..." }
```

### Chat (protetto)
`POST /chat` (Bearer token richiesto)
```json
{
  "model": "llama3",
  "prompt": "Ciao, chi sei?"
}
Risposta: { "response": "..." }
```

### Cronologia (protetto)
`GET /history` (Bearer token richiesto)
Risposta:
```json
[
  {
    "prompt": "Ciao, chi sei?",
    "response": "Sono un modello AI...",
    "model": "llama3",
    "timestamp": "2025-07-25T10:00:00"
  }
]
```

## Note tecniche
- **Password**: hashate con `werkzeug.security`.
- **JWT**: validità 1 ora.
- **Ollama**: endpoint locale `http://localhost:11434/api/chat`.
- **ORM**: SQLAlchemy, tabelle `users` e `messages`.
- **Logging e validazioni**: basilari, facilmente estendibili.

## Avvio in Docker (opzionale)
```sh
docker build -t ollama-chat .
docker run -p 5000:5000 --env-file .env ollama-chat
```

## Test API
Usa Postman o simili. Ricorda di:
- Registrare un utente
- Fare login e copiare il token JWT
- Usare il token come `Bearer` per `/chat` e `/history`

---

**Progetto didattico**: commenti e codice pensati per essere facilmente estendibili e comprensibili.
