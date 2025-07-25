import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Carica variabili ambiente dal file .env
load_dotenv()

db_url = os.getenv("DATABASE_URL")

# Crea l'engine SQLAlchemy
engine = create_engine(db_url)

try:
    with engine.connect() as conn:
        result = conn.execute("SELECT 1")
        print("Connessione OK! Risultato:", result.scalar())
except Exception as e:
    print("Errore di connessione:", e)
