# Vågen-match

Vågen-match er en sosial webapplikasjon for elever på Vågen videregående
skole. Elever kan opprette en konto, lage en profil, oppdage andre elever og
sende private meldinger.

Applikasjonen er laget som en prototype. Målet har vært å vise en tydelig
brukerflyt, server-side validering, sikker passordlagring og en løsning som
kan kjøres med PostgreSQL i Docker.

## Funksjonalitet

En innlogget bruker kan:

- registrere seg med et unikt brukernavn og passord
- logge inn og ut
- opprette eller oppdatere en profil
- velge linje og trinn fra en forhåndsdefinert liste
- se andre ferdige profiler på siden «Discover»
- åpne en privat chat med en annen bruker
- hente tidligere meldinger og motta nye meldinger i sanntid

Brukeren blir ikke vist sin egen profil i «Discover». Profil- og
chat-funksjonene krever innlogging.

## Teknologier

- **Python 3.12**
- **Flask** for HTTP-ruter og HTML-rendering
- **Flask-SocketIO** for sanntidsmeldinger
- **Jinja** for dynamisk innhold i malene
- **PostgreSQL** for brukere, profiler og meldinger
- **psycopg** for tilkobling til PostgreSQL
- **HTML, CSS og JavaScript** for brukergrensesnittet
- **Docker Compose** for lokal kjøring med webserver og database

Passord lagres ikke i klartekst. `werkzeug.security` brukes til å lage og
kontrollere passord-hasher.

## Prosjektstruktur

```text
.
├── app.py                 # Flask-applikasjon, ruter, validering og databasekall
├── templates/             # Jinja-maler for sidene
├── static/
│   ├── css/style.css      # Stil og layout
│   └── js/chat.js         # Klientkode for privat chat
├── Dockerfile             # Image for webapplikasjonen
├── docker-compose.yml     # Web- og PostgreSQL-tjeneste
├── pyproject.toml         # Python-avhengigheter og prosjektmetadata
└── run.bat                # Enkel DEV_MODE-start på Windows
```

## Kom i gang med Docker

### Forutsetninger

- Docker Desktop med Docker Compose
- Git, hvis prosjektet skal klones

Lag en lokal fil som heter `secret.env`. Filen skal ikke committes eller deles:

```env
SECRET_KEY=generer-en-lang-tilfeldig-verdi
DB_PASSWORD=generer-en-annen-lang-tilfeldig-verdi
```

Start webapplikasjonen og PostgreSQL:

```bash
docker compose --env-file secret.env up -d --build
```

Åpne deretter [http://localhost:5000](http://localhost:5000). Flask oppretter
tabellene `users`, `profiles` og `messages` automatisk når webtjenesten
starter. PostgreSQL-data lagres i Docker-volumet `postgres_data`.

Nyttige kommandoer:

```bash
docker compose ps
docker compose logs -f web
docker compose down
```

`docker compose down` stopper og fjerner containerne, men beholder normalt
volumet. Bruk `docker compose down -v` bare hvis databasen og alle dataene
skal slettes.

## Lokal utvikling på Windows

`run.bat` starter Flask med `DEV_MODE=1` og kjører:

```text
uv run app.py
```

Dette gjør det mulig å arbeide med HTML og CSS uten en lokal PostgreSQL-server.
I denne modusen hoppes databaseinitialiseringen over, så funksjoner som
registrering, innlogging, profiler og chat krever en tilgjengelig database og
skal testes med Docker Compose.

For lokal kjøring må [uv](https://docs.astral.sh/uv/) være installert. Kjør
`run.bat` fra prosjektmappen og åpne [http://127.0.0.1:5000](http://127.0.0.1:5000).

## Brukerflyt

1. På forsiden velger brukeren registrering eller innlogging.
2. Ved registrering kontrolleres at brukernavn og passord er fylt ut,
   brukernavnet er høyst 30 tegn, passordet har minst fire tegn og
   brukernavnet ikke allerede finnes.
3. Etter innlogging kan brukeren åpne «My Profile» og lagre navn, alder, linje,
   trinn og kjønn.
4. Profilen må ha navn på maksimalt 60 tegn, alder mellom 16 og 67 år, en
   gyldig linje og et gyldig kjønn.
5. På «Discover» vises andre brukere som har lagret en profil.
6. Fra en profil kan brukeren åpne «Send melding». Meldinger på mellom 1 og
   2000 tegn lagres i PostgreSQL og sendes til chatten i sanntid.
7. «Log out» fjerner innloggingsøkten og sender brukeren tilbake til forsiden.

## Hvordan koden er bygget opp

Hovedlogikken ligger i [`app.py`](./app.py):

- `/` viser forsiden.
- `/register` håndterer registrering.
- `/login` håndterer innlogging og oppretter en Flask-session.
- `/user` viser siden for innloggede brukere.
- `/profile` viser og lagrer profilinformasjon.
- `/discover` henter andre profiler.
- `/chat/<username>` viser privat chat.
- `/api/conversations/<username>` returnerer tidligere meldinger som JSON.
- `/logout` avslutter økten.
- Socket.IO-hendelsene `join_room` og `send_private_message` håndterer
  private rom og nye meldinger.

Ved oppstart bruker `init_db()` `CREATE TABLE IF NOT EXISTS` for å opprette
tabellene. Relasjonene mellom brukere, profiler og meldinger håndheves av
PostgreSQL, og sletting av en bruker sletter tilhørende profil og meldinger
med `ON DELETE CASCADE`.

## Begrensninger og videreutvikling

Dette er fortsatt en prototype. Før produksjonsbruk bør prosjektet blant annet:

- bruke en separat migreringsløsning i stedet for å opprette tabeller direkte
  ved oppstart
- få CSRF-beskyttelse, rate limiting og strengere sesjonskonfigurasjon
- få funksjoner for rapportering og blokkering
- få søk og filtrering på profiler
- få e-postbekreftelse og funksjon for glemt passord
- få bedre tilgjengelighet og flere automatiserte tester
- få en plan for sikkerhetskopiering, overvåking og databasevedlikehold

`SECRET_KEY`, `DB_PASSWORD` og andre hemmeligheter skal alltid komme fra
miljøvariabler eller en lokal hemmelighetsfil. Hemmeligheter som har blitt
delt eller committet må roteres.

## Sikkerhetskopiering

Ta sikkerhetskopi av PostgreSQL før vedlikehold eller produksjonsendringer:

```bash
docker compose --env-file secret.env exec -T db \
  pg_dump -U vagen_user -d vagen_match > vagen_match.sql
```

Sikkerhetskopifilen kan inneholde personopplysninger og må behandles
konfidensielt.
