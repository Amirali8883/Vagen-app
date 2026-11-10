from datetime import date
import os
import importlib
from contextlib import contextmanager

from flask import Flask, flash, jsonify, redirect, url_for, render_template, request, session
from flask_socketio import SocketIO, emit, join_room

from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
socketio = SocketIO(app)

app.secret_key = os.environ.get("SECRET_KEY", "dev-only-secret")
DATABASE_URL = os.environ.get("DATABASE_URL", "")

# DEV_MODE=1 skips the database entirely so you can work on HTML/CSS locally
# without needing a running PostgreSQL server.
DEV_MODE = os.environ.get("DEV_MODE", "0") == "1"

# Load the optional database driver dynamically so editors that do not have
# the project's dependencies installed do not report a false missing import.
if not DEV_MODE:
    psycopg = importlib.import_module("psycopg")


@contextmanager
def get_db():
    if DEV_MODE:
        raise RuntimeError("Database is disabled in DEV_MODE")
    with psycopg.connect(DATABASE_URL) as connection:
        yield connection


def init_db():
    if DEV_MODE:
        print("DEV_MODE: skipping database init")
        return
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
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS messages (
                id BIGSERIAL PRIMARY KEY,
                sender_id VARCHAR(30) NOT NULL REFERENCES users(username)
                    ON DELETE CASCADE,
                recipient_id VARCHAR(30) NOT NULL REFERENCES users(username)
                    ON DELETE CASCADE,
                content TEXT NOT NULL CHECK (char_length(content) BETWEEN 1 AND 2000),
                timestamp TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
                CHECK (sender_id <> recipient_id)
            )
            """
        )
        connection.execute(
            """
            CREATE INDEX IF NOT EXISTS messages_conversation_timestamp_idx
            ON messages (sender_id, recipient_id, timestamp)
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


def private_room(username_a, username_b):
    return f"chat_{min(username_a, username_b)}_{max(username_a, username_b)}"


def user_exists(username):
    with get_db() as connection:
        return connection.execute(
            "SELECT 1 FROM users WHERE username = %s",
            (username,)
        ).fetchone() is not None


@app.route("/chat/<username>")
def chat(username):
    current_username = session.get("user")
    if not current_username:
        return redirect(url_for("login"))
    if username == current_username or not user_exists(username):
        return redirect(url_for("discover"))

    return render_template(
        "chat.html",
        current_username=current_username,
        recipient_username=username,
    )


@app.route("/api/conversations/<username>")
def conversation_history(username):
    current_username = session.get("user")
    if not current_username:
        return jsonify({"error": "Authentication required"}), 401
    if username == current_username or not user_exists(username):
        return jsonify({"error": "User not found"}), 404

    with get_db() as connection:
        rows = connection.execute(
            """
            SELECT sender_id, recipient_id, content, timestamp
            FROM messages
            WHERE (sender_id = %s AND recipient_id = %s)
               OR (sender_id = %s AND recipient_id = %s)
            ORDER BY timestamp ASC, id ASC
            """,
            (current_username, username, username, current_username)
        ).fetchall()

    return jsonify([
        {
            "sender_id": row[0],
            "recipient_id": row[1],
            "content": row[2],
            "timestamp": row[3].isoformat(),
        }
        for row in rows
    ])


@socketio.on("join_room")
def handle_join_room(data):
    current_username = session.get("user")
    recipient_username = data.get("recipient_id") if isinstance(data, dict) else None

    if not current_username:
        emit("chat_error", {"message": "Authentication required"})
        return
    if (
        not isinstance(recipient_username, str)
        or recipient_username == current_username
        or not user_exists(recipient_username)
    ):
        emit("chat_error", {"message": "Invalid recipient"})
        return

    join_room(private_room(current_username, recipient_username))


@socketio.on("send_private_message")
def handle_private_message(data):
    current_username = session.get("user")
    recipient_username = data.get("recipient_id") if isinstance(data, dict) else None
    raw_content = data.get("content") if isinstance(data, dict) else None
    content = raw_content.strip() if isinstance(raw_content, str) else ""

    if not current_username:
        emit("chat_error", {"message": "Authentication required"})
        return
    if (
        not isinstance(recipient_username, str)
        or recipient_username == current_username
        or not user_exists(recipient_username)
    ):
        emit("chat_error", {"message": "Invalid recipient"})
        return
    if not content or len(content) > 2000:
        emit("chat_error", {"message": "Message must contain 1 to 2000 characters"})
        return

    with get_db() as connection:
        row = connection.execute(
            """
            INSERT INTO messages (sender_id, recipient_id, content)
            VALUES (%s, %s, %s)
            RETURNING sender_id, recipient_id, content, timestamp
            """,
            (current_username, recipient_username, content)
        ).fetchone()

    socketio.emit(
        "private_message",
        {
            "sender_id": row[0],
            "recipient_id": row[1],
            "content": row[2],
            "timestamp": row[3].isoformat(),
        },
        to=private_room(current_username, recipient_username),
    )


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
            SELECT username, name, age, linje, gender
            FROM profiles
            WHERE username <> %s
            ORDER BY username
            """,
            (session["user"],)
        ).fetchall()

    profiles = [
        {
            "username": row[0],
            "name": row[1],
            "age": row[2],
            "linje": row[3],
            "gender": row[4],
        }
        for row in rows
    ]

    return render_template(
        "discover.html",
        profiles=profiles
    )




if __name__ == '__main__':
    socketio.run(
        app,
        host="0.0.0.0",
        port=5000,
        allow_unsafe_werkzeug=True,
    )