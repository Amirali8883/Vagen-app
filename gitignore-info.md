# Merknader om `.gitignore`

Dette repositoriet inneholder en `.gitignore` med fornuftige standardinnstillinger for Python, `uv`, Node.js, IDE-er og vanlige utviklingsverktøy.

Du trenger normalt ikke å endre den.

## Miljøvariabler / hemmeligheter

`.env` og andre `.env.*`-filer ignoreres som standard.

`.env.example`, `.env.sample` og `.env.template` er tillatt.

Bruk disse til å dokumentere hvilke miljøvariabler som kreves:

```text
.env.example    # Commit denne
.env            # Ikke commit denne
````

Ikke legg ekte passord, API-nøkler, tokens eller andre hemmeligheter i `.env.example`.

Hvis du **spesifikt må levere en `.env`-fil som en del av en oppgave**, kan du tvinge Git til å legge den til:

```bash
git add -f .env
```

Gjør dette bare dersom du uttrykkelig har fått beskjed om å levere filen, og den ikke inneholder sensitiv informasjon.

## `uv`

`uv.lock` ignoreres **ikke**, og skal normalt committes.

`.venv/` ignoreres.

Et typisk prosjekt:

```text
pyproject.toml    # Commit
uv.lock           # Commit
.venv/            # Ikke commit
```

## IDE-er

IDE-konfigurasjon ignoreres:

```text
.idea/
.vscode/
```

Du kan bruke PyCharm, VS Code, Cursor osv. uten å committe lokal konfigurasjon.

## Python-cacher

Genererte Python-filer ignoreres:

```text
__pycache__/
*.pyc
.pytest_cache/
.ruff_cache/
.mypy_cache/
.pyright/
```

Du trenger ikke å slette disse manuelt før du committer.

## Jupyter

Notebook-filer (`.ipynb`) ignoreres **ikke** og kan committes.

Kun genererte Jupyter checkpoint-filer ignoreres:

```text
.ipynb_checkpoints/
```

## Node.js

Hvis du bruker Node.js/JavaScript/TypeScript:

```text
node_modules/
```

ignoreres.

Commit filer som:

```text
package.json
package-lock.json
```

men ikke `node_modules/`.

## Byggfiler

Vanlige genererte mapper som disse ignoreres:

```text
build/
dist/
out/
target/
tmp/
temp/
```

## Lokale databaser

Vanlige lokale databasefiler ignoreres:

```text
*.db
*.sqlite
*.sqlite3
```

Filer som `.csv`, `.json` og `.yaml` ignoreres **ikke** globalt, siden de kan være en del av en oppgave.

## Logger / midlertidige filer

Vanlige logger og midlertidige filer ignoreres:

```text
*.log
*.tmp
*.bak
*.swp
```

## Hvorfor ignorerer Git filen min?

Hvis en fil ikke vises når du kjører:

```bash
git status
```

kan du sjekke hvorfor med:

```bash
git check-ignore -v sti/til/fil
```

For eksempel:

```bash
git check-ignore -v .env
```

## Viktig

`.gitignore` fjerner ikke filer som allerede har blitt committed.

Hvis du ved et uhell committer et passord, en API-nøkkel eller en annen hemmelighet, **må du ikke anta at det er nok å bare slette filen**. Roter/tilbakekall hemmeligheten umiddelbart.

For vanlige oppgaver kan du stort sett følge denne regelen:

```text
Commit:
  Kildekode
  README/dokumentasjon
  pyproject.toml
  uv.lock
  Tester
  Notebooks
  Data/filer som er en del av oppgaven

Ikke commit:
  .env
  .venv/
  __pycache__/
  .pytest_cache/
  .ruff_cache/
  .idea/
  .vscode/
  node_modules/
  Byggfiler
  Logger
  Lokale databaser
```
