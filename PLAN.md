# Piano di sviluppo e verifica: Ollama Chat API

## 1. Preparazione ambiente
- [x] Installare Python 3.10+
- [x] Installare SQL Server e creare database dedicato
- [x] Installare/avviare Ollama in locale (es: `ollama serve`)
- [x] Clonare/scaricare il progetto
- [x] Copiare `.env.example` in `.env` e configurare credenziali DB/JWT
- [x] Installare le dipendenze:
  ```sh
  pip install -r requirements.txt
  ```

## 2. Database e modelli
- [x] Verificare la connessione a SQL Server (`DATABASE_URL`)
- [x] Creare le tabelle (`users`, `messages`) tramite SQLAlchemy
- [x] Testare la creazione automatica delle tabelle (es. con `flask shell` o script)

## 3. Autenticazione e utenti
- [x] Testare endpoint `/auth/register` (registrazione utente)
- [x] Testare endpoint `/auth/login` (ricezione JWT valido)
- [x] Verificare hash password e validità JWT (1h)

## 4. Chat e cronologia
- [x] Testare endpoint protetto `/chat`:
    - [x] Invio prompt e scelta modello (es: `llama3`, `mistral`)
    - [x] Ricezione risposta da Ollama
    - [x] Salvataggio prompt, risposta, modello, timestamp, utente
- [x] Testare endpoint protetto `/history`:
    - [x] Recupero cronologia messaggi utente

## 5. Validazioni, errori e logging
- [x] Verificare gestione errori (dati mancanti, credenziali errate, errori Ollama)
- [x] Verificare logging basilare (console/log file)
- [x] Validare input (username, email, password, prompt, modello)

## 6. Test end-to-end API
- [x] Usare Insomnia per:
    - [x] Registrare utente
    - [x] Login e recupero token
    - [x] Chiamare `/chat` e `/history` con token Bearer
    - [x] Verificare risposte e salvataggio dati

## 7. Docker e deploy (opzionale)
- [ ] Costruire immagine Docker
- [ ] Avviare container con variabili ambiente
- [ ] Verificare funzionamento API in container

## 8. Migliorie e sicurezza (consigliato)
- [x] Aggiungere logging avanzato (file, livelli)
- [x] Rate limiting sugli endpoint
- [x] Migliorare validazione input (regex, email, password forti)
- [x] Gestione refresh token JWT
- [x] Documentazione OpenAPI/Swagger

---

**Nota:** Ogni step va testato singolarmente prima di procedere al successivo. Spuntare ogni voce solo dopo verifica effettiva.

