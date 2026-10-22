from flask import Flask, flash, redirect, url_for, render_template, request, session, flash


app = Flask(__name__)

app.secret_key = "the_secret_key"  

@app.route('/')
def home():
    return render_template('home.html')

users = {
    "amir": "1234",
    "student": "password123",
    "test": "test123"
}

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        name = request.form.get("name", "").strip().lower()
        password = request.form.get("password", "")

        if name in users and users[name] == password:
            session["user"] = name
            return redirect(url_for("user"))

        flash("Feil brukernavn eller passord. Prøv igjen.")
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