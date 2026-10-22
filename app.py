import json
from pathlib import Path
from datetime import date

from flask import Flask, flash, redirect, url_for, render_template, request, session 

from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.secret_key = "the_secret_key"  

DATA_DIR = Path(app.root_path) / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

DB_FILE = DATA_DIR / "userdb.json"
PROFILES_FILE = DATA_DIR / "profiles.json"

def load_users():
    if not DB_FILE.exists():
        DB_FILE.write_text(
            json.dumps({"users": []}, indent=4),
            encoding="utf-8"
        )

    with DB_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)



def save_users(data):
    with DB_FILE.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

LINJE_OPTIONS = [
       # Studiespesialisering
    "Vg1 - Studiespesialisering",
    "Vg2 - Studiespesialisering",
    "Vg3 - Studiespesialisering",

    # Informasjonsteknologi og medieproduksjon
    "Vg1 - Informasjonsteknologi og medieproduksjon",
    "Vg2 - Informasjonsteknologi",
    "Vg2 - Medieproduksjon",
    "Vg3 - IT-driftsfaget",
    "Vg3 - Innholdsproduksjonsfaget",

    # Kunst, design og arkitektur
    "Vg1 - Kunst, design og arkitektur",
    "Vg2 - Kunst, design og arkitektur",
    "Vg3 - Kunst, design og arkitektur",

    # Musikk, dans og drama
    "Vg1 - Musikk, dans og drama",
    "Vg2 - Musikk",
    "Vg2 - Dans",
    "Vg2 - Drama",
    "Vg3 - Musikk",
    "Vg3 - Dans",
    "Vg3 - Drama",

    # Other programmes (examples)
    "Vg1 - Elektro og datateknologi",
    "Vg2 - Elenergi og ekom",
    "Vg1 - Teknologi- og industrifag",
    "Vg2 - Industriteknologi",
    "Vg1 - Helse- og oppvekstfag",
    "Vg2 - Barne- og ungdomsarbeiderfag",
    "Vg1 - Bygg- og anleggsteknikk",
    "Vg1 - Salg, service og reiseliv",
    
]


GENDER_OPTIONS = ["man", "women", "other"]


def load_profiles():
    if not PROFILES_FILE.exists():
        PROFILES_FILE.write_text(
            json.dumps({"profiles": {}}, indent=4),
            encoding="utf-8"
        )

    with PROFILES_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_profiles(data):
    with PROFILES_FILE.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
        
@app.route('/')
def home():
    return render_template('home.html')



@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("name", "").strip().lower()
        password = request.form.get("password", "")

        if not username or not password:
            flash("Fyll inn både brukernavn og passord.")
            return redirect(url_for("register"))

        if len(username) > 30 or len(password) < 4:
            flash("Brukernavnet kan maks være 30 tegn. Passordet må ha minst 4 tegn.")
            return redirect(url_for("register"))

        data = load_users()

        # Check whether the username already exists
        for user in data["users"]:
            if user["username"].lower() == username:
                flash("Brukernavnet er allerede i bruk.")
                return redirect(url_for("register"))

        # Create and save the new account
        new_user = {
            "username": username,
            "password": generate_password_hash(password),
            "date": date.today().isoformat()
        }

        data["users"].append(new_user)
        save_users(data)

        flash("Kontoen din er opprettet! Du kan logge inn.")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("name", "").strip().lower()
        password = request.form.get("password", "")

        data = load_users()

        for user in data["users"]:
            if (
                user["username"].lower() == username
                and check_password_hash(user["password"], password)
            ):
                session.clear()
                session["user"] = user["username"]
                return redirect(url_for("user"))

        flash("Feil brukernavn eller passord.")
        return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/user")
def user():
    if "user" not in session:
        return redirect(url_for("login"))

    return render_template("user.html", name=session["user"])

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("home"))



@app.route("/profile", methods=["GET", "POST"])
def profile():
    if "user" not in session:
        return redirect(url_for("login"))

    username = session["user"]
    data = load_profiles()

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        age_text = request.form.get("age", "").strip()
        linje = request.form.get("linje", "")
        gender = request.form.get("gender", "")

        try:
            age = int(age_text)
        except ValueError:
            age = 0

        if not name or len(name) > 60:
            flash("Skriv inn et navn på maks 60 tegn.")
        elif not 16 <= age <= 67:
            flash("Alderen må være mellom 16 og 67 år.")
        elif linje not in LINJE_OPTIONS:
            flash("Velg en gyldig linje.")
        elif gender not in GENDER_OPTIONS:
            flash("Velg et gyldig kjønn.")
        else:
            data["profiles"][username] = {
                "name": name,
                "age": age,
                "linje": linje,
                "gender": gender
            }

            save_profiles(data)
            flash("Profilen din er lagret!")
            return redirect(url_for("profile"))

    profile_data = data["profiles"].get(username, {})

    return render_template(
        "profile.html",
        profile=profile_data,
        linje_options=LINJE_OPTIONS,
        gender_options=GENDER_OPTIONS
    )


@app.route("/discover")
def discover():
    if "user" not in session:
        return redirect(url_for("login"))

    data = load_profiles()
    profiles = []

    for username, profile_data in data["profiles"].items():
        if username == session["user"]:
            continue

        if profile_data.get("name"):
            profiles.append(profile_data)

    return render_template(
        "discover.html",
        profiles=profiles
    )

if __name__ == '__main__':
    app.run(debug=True)