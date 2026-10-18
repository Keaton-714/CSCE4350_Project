from pathlib import Path
from flask import Flask, redirect, render_template, request, session, url_for

# This section of code is to find the frontend files (for now login and main)  
FRONTEND = Path(__file__).resolve().parent.parent / "frontend"
app = Flask(
    __name__,
    template_folder=str(FRONTEND / "templates"),
    static_folder=str(FRONTEND / "static"),
)
app.secret_key = "change-me" # temporary for know 

# This is the hardcode password and username just for test for login (temporary)
USERNAME = "demo"
PASSWORD = "password"

# Code is for confirming the password and username is correct  
@app.route("/", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        if request.form["username"] == USERNAME and request.form["password"] == PASSWORD:
            session["user"] = USERNAME
            return redirect(url_for("main"))
        error = "Incorrect username or password."
    return render_template("login.html", error=error)


@app.route("/main")
def main():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("main.html", user=session["user"])

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)