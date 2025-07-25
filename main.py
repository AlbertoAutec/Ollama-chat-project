# Entry point dell'applicazione Flask
from app import create_app

app = create_app()

if __name__ == "__main__":
    # Avvia il server Flask
    app.run(debug=True, host="0.0.0.0", port=5000)
