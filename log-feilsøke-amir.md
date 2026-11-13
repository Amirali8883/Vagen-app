## Felles navbar med Jinja

Problemet var at `chat.html` hadde sin egen, korte header. Den viste bare
logoen og «Logg ut», mens `discover.html` og `profile.html` hadde andre
kopier av navigasjonsmenyen. Når navigasjonen finnes i flere filer, kan
sidene lett få forskjellige lenker eller ulik oppførsel.

Løsningen er å samle menyen i:

```text
templates/_navbar.html
```

Dette er en Jinja-partial. Den inneholder hele `<header>`-elementet,
Home-, Discover-, My Profile- og login/logout-lenkene, samt JavaScript-filen
for mobilmenyen.

### Hvordan den brukes

Forsiden bruker mal-arv. I `home.html` står:

```jinja
{% extends "base.html" %}
```

`base.html` bygger den felles HTML-strukturen og inkluderer partialen:

```jinja
{% include "_navbar.html" %}
```

De andre sidene har en egen HTML-struktur og inkluderer derfor partialen
direkte, for eksempel i `chat.html`:

```jinja
{% include "_navbar.html" %}
```

Jinja setter inn innholdet i `_navbar.html` før Flask sender ferdig HTML til
nettleseren. Nettleseren ser derfor ikke `include`-kommandoen; den får bare
den ferdige headeren.

### Dynamiske lenker

Navbar-partialen bruker Flask- og Jinja-verdier:

```jinja
{% if session.get('user') %}
    Vis brukernavn og Log out
{% else %}
    Vis Login
{% endif %}
```

`session.get('user')` viser om brukeren er innlogget. `request.endpoint`
sammenlignes med den aktive ruten, slik at riktig menylenke får CSS-klassen
`active`. For eksempel blir Discover markert når `request.endpoint` er
`discover`.

Discover og My Profile bruker også denne regelen:

```jinja
{{ url_for('discover') if session.get('user') or DEV_MODE else url_for('login') }}
```

En innlogget bruker får den faktiske ruten. En bruker uten innlogging sendes
til login, mens `DEV_MODE=1` tillater forhåndsvisning under lokal
HTML/CSS-utvikling.

### Hvorfor dette løser chat-problemet

`chat.html` inkluderer nå samme `_navbar.html` som de andre sidene. Derfor
har chat-siden også lenker til Home, Discover og My Profile, i tillegg til
brukernavn og Log out når brukeren er innlogget. Endringer i navigasjonen må
bare gjøres i én fil.

Hamburgerknappen bruker `id="menuToggle"` og navigasjonen bruker
`id="navBar"`. `static/js/script.js` finner disse elementene og legger til
eller fjerner klassen `open` når knappen trykkes på. Siden scriptet også
inkluderes fra partialen, fungerer mobilmenyen på alle sider som bruker
navbar-partialen.