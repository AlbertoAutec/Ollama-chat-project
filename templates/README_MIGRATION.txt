I file HTML sono stati spostati dalla root del progetto alla cartella templates/.

Se usavi i file chat.html, login.html, register.html, history.html dalla root, ora si trovano in templates/.

Non è necessario aggiornare il codice Flask se non usavi render_template, poiché il frontend viene servito staticamente o tramite browser.

Se vuoi servire queste pagine direttamente da Flask, usa:
from flask import render_template

@app.route('/login')
def login():
    return render_template('login.html')

E così via per le altre pagine.
