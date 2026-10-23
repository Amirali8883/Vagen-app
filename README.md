# ✨ Prosjektnavn (Python)

Instansier prosjektet ved å først kjøre `uv sync` og deretter `uv venv`

> [!IMPORTANT]
> **README.md – endre denne filen!**
>
> Behold `.gitignore` og `.gitattributes` i prosjektet.

> [!NOTE]
> Denne filen er en plassholder. Skriv en kort beskrivelse av prosjektet her.
>
> Som et minimum bør en README inneholde:
>
> - En kort presentasjon av prosjektet
> - Hvordan prosjektet installeres
> - Hvordan prosjektet kjøres
>
> Legg gjerne til annen informasjon som er relevant for prosjektet.

## 📁 Viktige filer i repoet

> [!TIP]
> Disse filene er en del av grunnoppsettet og bør beholdes:
>
> - `.gitignore` – hindrer at midlertidige filer, lokale miljøer og hemmeligheter blir lagt til i Git.
> - `.gitattributes` – sørger blant annet for konsistent håndtering av linjeskift på tvers av operativsystemer.

## Kjør med Docker

Installer og start [Docker Desktop](https://www.docker.com/products/docker-desktop/), og kjør deretter
følgende kommandoer fra prosjektmappen:

```sh
docker compose up --build
```

Åpne <http://localhost:5000> i nettleseren. Stopp containeren med `Ctrl+C`, eller kjør
`docker compose down` fra en annen terminal.

Compose monterer prosjektets `data/`-mappe inn i containeren, slik at registrerte brukere og
profiler beholdes når containeren startes på nytt. `DOCKERFILE` installerer avhengighetene fra
`requirements.txt` og starter Flask-appen med Gunicorn på port 5000.


feilsøking: hvordan få jeg bruker sin nav og passordet ble registert? json fil og database.

chat system, bio, hobbies, filter etter kjønn og linje, profil bilde, rate limiter, ai profile picture protection,  
eadme instalsjon , update,