from datetime import date
import os
from contextlib import contextmanager

import psycopg
from flask import Flask, flash, redirect, url_for, render_template, request, session

from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.secret_key = os.environ["SECRET_KEY"]
DATABASE_URL = os.environ["DATABASE_URL"]


@contextmanager
def get_db():
    with psycopg.connect(DATABASE_URL) as connection:
        yield connection


def init_db():
    with get_db() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                username VARCHAR(30) PRIMARY KEY,
                password_hash TEXT NOT NULL,
                created_at DATE NOT NULL
            )
            """
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS profiles (
                username VARCHAR(30) PRIMARY KEY REFERENCES users(username)
                    ON DELETE CASCADE,
                name VARCHAR(60) NOT NULL,
                age INTEGER NOT NULL CHECK (age BETWEEN 16 AND 67),
                linje TEXT NOT NULL,
                gender VARCHAR(20) NOT NULL
            )
            """
        )


init_db()

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

        with get_db() as connection:
            existing_user = connection.execute(
                "SELECT 1 FROM users WHERE username = %s",
                (username,)
            ).fetchone()
            if existing_user:
                flash("Brukernavnet er allerede i bruk.")
                return redirect(url_for("register"))

            connection.execute(
                """
                INSERT INTO users (username, password_hash, created_at)
                VALUES (%s, %s, %s)
                """,
                (username, generate_password_hash(password), date.today())
            )

        flash("Kontoen din er opprettet! Du kan logge inn.")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("name", "").strip().lower()
        password = request.form.get("password", "")

        with get_db() as connection:
            user = connection.execute(
                "SELECT username, password_hash FROM users WHERE username = %s",
                (username,)
            ).fetchone()

        if user and check_password_hash(user[1], password):
            session.clear()
            session["user"] = user[0]
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
            with get_db() as connection:
                connection.execute(
                    """
                    INSERT INTO profiles (username, name, age, linje, gender)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (username) DO UPDATE SET
                        name = EXCLUDED.name,
                        age = EXCLUDED.age,
                        linje = EXCLUDED.linje,
                        gender = EXCLUDED.gender
                    """,
                    (username, name, age, linje, gender)
                )
            flash("Profilen din er lagret!")
            return redirect(url_for("profile"))

    with get_db() as connection:
        profile = connection.execute(
            """
            SELECT name, age, linje, gender
            FROM profiles
            WHERE username = %s
            """,
            (username,)
        ).fetchone()

    profile_data = (
        {"name": profile[0], "age": profile[1], "linje": profile[2], "gender": profile[3]}
        if profile
        else {}
    )

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

    with get_db() as connection:
        rows = connection.execute(
            """
            SELECT name, age, linje, gender
            FROM profiles
            WHERE username <> %s
            ORDER BY username
            """,
            (session["user"],)
        ).fetchall()

    profiles = [
        {"name": row[0], "age": row[1], "linje": row[2], "gender": row[3]}
        for row in rows
    ]

    return render_template(
        "discover.html",
        profiles=profiles
    )




if __name__ == '__main__':
    app.run()