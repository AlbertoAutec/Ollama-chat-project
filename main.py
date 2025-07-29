
# Entry point dell'applicazione Flask

from app import create_app
from flask import render_template, redirect, url_for, session

app = create_app()

# Route logout utente
@app.route("/logout")
def logout():
    # Se usi sessione server-side, cancella la sessione
    session.clear()
    return redirect(url_for("login_page"))

# Route home page
@app.route("/")
def home_page():
    return render_template("login.html")

@app.route("/chat")
def chat_page():
    return render_template("chat.html")

@app.route("/register")
def register_page():
    return render_template("register.html")

@app.route("/login")
def login_page():
    return render_template("login.html")

@app.route("/history")
def history_page():
    return render_template("history.html")
