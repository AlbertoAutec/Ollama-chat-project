# Piano di sviluppo e verifica: Ollama Chat API

## 1. Preparazione ambiente
- [ ] Installare Python 3.10+
- [ ] Installare SQL Server e creare database dedicato
- [ ] Installare/avviare Ollama in locale (es: `ollama serve`)
- [ ] Clonare/scaricare il progetto
- [ ] Copiare `.env.example` in `.env` e configurare credenziali DB/JWT
- [ ] Installare le dipendenze:
  ```sh
  pip install -r requirements.txt
  ```

## 2. Database e modelli
- [ ] Verificare la connessione a SQL Server (`DATABASE_URL`)
- [ ] Creare le tabelle (`users`, `messages`) tramite SQLAlchemy
- [ ] Testare la creazione automatica delle tabelle (es. con `flask shell` o script)

## 3. Autenticazione e utenti
- [ ] Testare endpoint `/auth/register` (registrazione utente)
- [ ] Testare endpoint `/auth/login` (ricezione JWT valido)
- [ ] Verificare hash password e validità JWT (1h)

## 4. Chat e cronologia
- [ ] Testare endpoint protetto `/chat`:
    - [ ] Invio prompt e scelta modello (es: `llama3`, `mistral`)
    - [ ] Ricezione risposta da Ollama
    - [ ] Salvataggio prompt, risposta, modello, timestamp, utente
- [ ] Testare endpoint protetto `/history`:
    - [ ] Recupero cronologia messaggi utente

## 5. Validazioni, errori e logging
- [ ] Verificare gestione errori (dati mancanti, credenziali errate, errori Ollama)
- [ ] Verificare logging basilare (console/log file)
- [ ] Validare input (username, email, password, prompt, modello)

## 6. Test end-to-end API
- [ ] Usare Postman per:
    - [ ] Registrare utente
    - [ ] Login e recupero token
    - [ ] Chiamare `/chat` e `/history` con token Bearer
    - [ ] Verificare risposte e salvataggio dati

## 7. Docker e deploy (opzionale)
- [ ] Costruire immagine Docker
- [ ] Avviare container con variabili ambiente
- [ ] Verificare funzionamento API in container

## 8. Migliorie e sicurezza (consigliato)
- [ ] Aggiungere logging avanzato (file, livelli)
- [ ] Rate limiting sugli endpoint
- [ ] Migliorare validazione input (regex, email, password forti)
- [ ] Gestione refresh token JWT
- [ ] Documentazione OpenAPI/Swagger

---

**Nota:** Ogni step va testato singolarmente prima di procedere al successivo. Spuntare ogni voce solo dopo verifica effettiva.
