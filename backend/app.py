import re
from pathlib import Path
from flask import Flask, flash, redirect, render_template, request, session, url_for
from backend.routes.auth_routes import auth_bp # For auth_routes.py (authentication endpoint)

# This section of code is to find the frontend files (for now login and main)  
FRONTEND = Path(__file__).resolve().parent.parent / "frontend"
app = Flask(
    __name__,
    template_folder=str(FRONTEND / "templates"),
    static_folder=str(FRONTEND / "static"),
)
app.secret_key = "change-me" # temporary for know 

app.register_blueprint(auth_bp) # Needed to allow for the endpoint to exist in another module (outside of app.py)

# This is the hardcode password and username just for test for login (temporary)
USERNAME = "demo"
PASSWORD = "password"

# Sign up page (TEST ONLY): validates the form but does NOT store anything yet.
# Later this is where we would hash the password and INSERT into User/Customer.
SIGNUP_FIELDS = ["username", "first_name", "last_name", "street_address",
                 "city", "state", "zip", "phone", "email"]


@app.route("/main")
def main():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("main.html", user=session["user"])


if __name__ == "__main__":
    app.run(debug=True)