
# Entry point dell'applicazione Flask
from app import create_app
from flask import render_template

app = create_app()

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
