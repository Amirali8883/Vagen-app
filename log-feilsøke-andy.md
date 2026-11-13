Det er ikke mulig å jobbe med applikasjonen dersom Proxy Manager er nede.
I tillegg må jeg gjennom følgende prosess hver gang jeg gjør endringer i designet:

Commit --> Push --> Bygge et nytt Docker-image i Debian

Først etter dette kan jeg se endringene jeg har gjort i applikasjonen.
Løsning
I stedet vil jeg kjøre Docker-containeren lokalt i WSL (Windows Subsystem for Linux). På denne måten kan jeg gjøre endringer i koden og se dem oppdatert live via localhost, uten å måtte bygge et nytt Docker-image hver gang.
Når endringene er ferdige og testet lokalt, kan jeg pushe dem til repositoryet. Deretter kan Amir bygge et nytt Docker-image for den faktiske live-webapplikasjonen.
Implementering
Vi har lagt til en run.bat-fil.
Vi har implementert en egen Dev Mode.
Ved å kjøre docker compose up i WSL kan applikasjonen startes lokalt og nås via localhost.
Andreas legger til loggen etterpå.
10/11/2026