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

<<<<<<< HEAD
Noen sentrale deler er:

- `register()` håndterer oppretting av brukere.
- `login()` kontrollerer brukernavn og passord.
- `profile()` viser og lagrer profilinformasjon.
- `discover()` finner og viser andre profiler.
- `load_users()` og `save_users()` leser og lagrer brukere.
- `load_profiles()` og `save_profiles()` leser og lagrer profiler.

Flask-ruter bestemmer hvilken funksjon som skal kjøre når brukeren besøker en bestemt adresse, for eksempel `/login`, `/profile` eller `/discover`.

## 7. Validering og brukerfeedback

En viktig del av appen er at brukeren får beskjed når noe er feil. Eksempler på validering er:

- navn kan ikke være tomt eller lengre enn 60 tegn
- alder må være mellom 16 og 67 år
- linjen må være valgt fra listen over gyldige linjer
- kjønn må være et gyldig alternativ
- brukernavn må være unikt

Feilmeldinger vises med Flask `flash()` slik at brukeren forstår hva som må rettes.

## 8. Design og brukeropplevelse

Designet bruker en lys bakgrunn med rosa detaljer. Dette gir appen et vennlig og sosialt uttrykk.

Jeg har lagt vekt på:

- enkel navigasjon
- tydelige knapper
- korte skjemaer
- god avstand mellom elementene
- et språk som er lett å forstå
- et design som fungerer på både store og små skjermer

Målet er at brukeren skal forstå hva appen gjør uten å måtte lese mye informasjon først.

## 9. Hva som fungerer bra

Det som fungerer bra i løsningen er:

- brukerflyten er enkel å følge
- registrering og innlogging fungerer sammen
- brukeren kan lagre og oppdatere profilen sin
- bare innloggede brukere får tilgang til profil- og discover-sidene
- passord blir hashet før lagring
- profilene blir presentert på en oversiktlig måte
- løsningen er lett å videreutvikle

## 10. Begrensninger ved prototypen

Siden dette er en prototype, har løsningen noen begrensninger:

- data lagres i JSON-filer i stedet for en database
- det finnes ikke ekte meldinger mellom brukere
- brukere kan ikke filtrere eller søke etter profiler
- det finnes ikke e-postbekreftelse eller glemt passord
- løsningen har ikke et ferdig system for rapportering eller blokkering
- sikkerhet og personvern må styrkes før appen kan brukes i produksjon

JSON-filer passer godt for å demonstrere funksjonalitet, men en større applikasjon bør bruke en ordentlig database.

## 11. Mulig videreutvikling

Hvis jeg skulle jobbet videre med prosjektet, ville jeg prioritert:

1. Bytte ut JSON-lagringen med en database, for eksempel SQLite eller PostgreSQL.
2. Lage et meldingssystem mellom brukere.
3. Legge til søk og filtrering på linje, trinn og interesser.
4. La brukeren legge til interesser og et profilbilde.
5. Lage funksjoner for å blokkere og rapportere brukere.
6. Forbedre tilgjengelighet, blant annet tastaturnavigasjon og tydeligere kontraster.
7. Flytte hemmelige innstillinger, som Flask sin secret key, til miljøvariabler.

## 12. Avslutning

Vågen-match er en enkel prototype som viser hvordan en webapplikasjon kan hjelpe elever med å bli kjent med andre på skolen.

Løsningen har en tydelig brukerflyt, grunnleggende validering og lokal lagring av kontoer og profiler. Selv om appen kan forbedres med database, meldinger og bedre sikkerhet, viser prototypen de viktigste delene av en fungerende sosial webapplikasjon.

## 13. Produksjonsdatabase med Docker

### Lokal utvikling med automatisk oppdatering

For å se HTML-, CSS- og Python-endringer etter lagring, kjør `run.bat` og åpne
`http://127.0.0.1:5000`. Denne modusen har automatisk omlasting aktivert, men
`DEV_MODE=1` deaktiverer databasen. Forsiden og statiske filer kan derfor
vises, mens innlogging, profiler, discover og chat krever Docker-oppsettet
nedenfor.

Appen bruker PostgreSQL når den kjører med Docker Compose. `web`-containeren
kobler til `db`-containeren gjennom `DATABASE_URL`, og `users` og `profiles`
opprettes automatisk i PostgreSQL. Data ligger i Docker-volumet
`postgres_data`, ikke i web-containeren. Derfor kan flere web-containere dele
de samme kontoene og profilene.

Opprett en lokal `secret.env`-fil (den skal ikke committes):
=======
Lag en lokal fil som heter `secret.env`. Filen skal ikke committes eller deles:
>>>>>>> 959e7b0baec8b829130d2c07b67702c927a4ac22

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
