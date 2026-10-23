# dokumentasjon av Vågen-match

## 1. Innledning

**Vågen-match**, en enkel sosial webapplikasjon laget for elever på Vågen videregående skole.

Ideen bak appen er å gjøre det lettere for elever å bli kjent med hverandre. Mange elever kan synes det er vanskelig å ta kontakt med nye mennesker og fra andre linjer. Med Vågen-match kan man lage en profil og se andre elever som også ønsker å bli kjent med nye mennesker.

Appen er laget som en prototype. Det betyr at hovedfokuset har vært på funksjonalitet, brukerflyt og et oversiktlig design.

## 2. Problemstillingen

Problemstillingen var:

> Hvordan kan vi lage en enkel og trygg digital løsning som hjelper elever med å oppdage andre elever på skolen?

For å svare på dette laget vi en løsning med:
- må vere på ROGFK nettverket
- registrering og innlogging
- personlig profil
- valg av linje og trinn
- oversikt over andre profiler
- mulighet til å logge ut

## 3. Slik fungerer appen

Brukeren følger denne flyten:

1. Brukeren åpner forsiden.
2. Brukeren oppretter en konto med brukernavn og passord.
3. Brukeren logger inn.
4. Brukeren fyller ut profilen sin:
   - navn
   - alder
   - linje og trinn
   - kjønn
5. Profilen blir lagret.
6. Brukeren kan gå til «Discover» og se andre ferdige profiler.
7. Brukeren kan logge ut når som helst.

På denne måten får brukeren en tydelig og enkel brukeropplevelse fra registrering til ferdig profil.

## 4. Demonstrasjon
### Steg 1: Forsiden

vi starter på forsiden og viser navigasjonen. Herfra kan brukeren gå videre til registrering eller innlogging.

### Steg 2: Registrering

vi oppretter en ny bruker. Appen sjekker blant annet at:

- brukernavn og passord er fylt ut
- brukernavnet ikke er for langt
- passordet har minst fire tegn
- brukernavnet ikke allerede finnes

Hvis noe er feil, får brukeren en tydelig feilmelding.

### Steg 3: Innlogging

Etter registrering logger jeg inn med brukeren. Når innloggingen er godkjent, blir brukeren sendt til sin egen side.

Passordet lagres ikke som ren tekst. Det behandles med hashing ved hjelp av Werkzeug før det lagres.

### Steg 4: Lage profil

Jeg åpner profilsiden og fyller ut informasjonen min. Linje-feltet bruker en liste med tilgjengelige linjer og trinn, for eksempel:

- Studiespesialisering
- Informasjonsteknologi
- Kunst, design og arkitektur
- Musikk, dans og drama
- flere yrkesfaglige linjer

Appen validerer at navnet, alderen, linjen og kjønnet har gyldige verdier.

### Steg 5: Oppdage andre elever

Til slutt åpner jeg «Discover». Der vises andre elever som har laget en profil. Min egen profil blir ikke vist i listen, slik at brukeren bare ser andre profiler.

## 5. Teknologier

Appen er bygget med:

- **Python** som programmeringsspråk
- **Flask** som web-rammeverk
- **HTML** for sidene og skjemaene
- **CSS** for design og layout
- **Jinja** for dynamisk innhold i HTML-malene
- **JSON-filer** for enkel lagring av brukere og profiler

Prosjektet bruker også `pathlib` for å håndtere filstier på en ryddig måte.

Datafilene ligger samlet i en lokal `data`-mappe:

```text
data/
├── userdb.json
└── profiles.json
```

Dette gjør at brukerkontoer og profiler blir lagret på samme sted i prosjektet.

## 6. Hvordan koden er bygget opp

Hovedlogikken ligger i `app.py`.

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

