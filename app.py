import json
from pathlib import Path
from datetime import date

from flask import Flask, flash, redirect, url_for, render_template, request, session, 

from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.secret_key = "the_secret_key"  

DB_FILE = Path(app.root_path) / "userdb.json"

DATA_DIR = Path("/app/data")
DATA_DIR.mkdir(parents=True, exist_ok=True)

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

if __name__ == '__main__':
    app.run(debug=True)