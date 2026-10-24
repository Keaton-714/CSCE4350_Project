import re
from pathlib import Path
from flask import Flask, flash, redirect, render_template, request, session, url_for

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


# Sign up page (TEST ONLY): validates the form but does NOT store anything yet.
# Later this is where we would hash the password and INSERT into User/Customer.
SIGNUP_FIELDS = ["username", "first_name", "last_name", "street_address",
                 "city", "state", "zip", "phone", "email"]

@app.route("/signup", methods=["GET", "POST"])
def signup():
    errors = []
    form = {f: "" for f in SIGNUP_FIELDS}  # used to refill the form if there are errors
    if request.method == "POST":
        form = {f: request.form.get(f, "").strip() for f in SIGNUP_FIELDS}
        password = request.form.get("password", "")
        confirm = request.form.get("confirm_password", "")

        # This section of code will check that each field are accurate 
        for f in SIGNUP_FIELDS:
            if not form[f]:
                errors.append(f"{f.replace('_', ' ').title()} is required.")
        if len(password) < 8:
            errors.append("Password must be at least 8 characters.")
        if password != confirm:
            errors.append("Passwords do not match.")
        if form["email"] and not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", form["email"]):
            errors.append("Enter a valid e-mail address.")
        if form["phone"] and len(re.sub(r"\D", "", form["phone"])) != 10:
            errors.append("Phone number must have 10 digits.")
        if form["zip"] and not re.fullmatch(r"\d{5}", form["zip"]):
            errors.append("ZIP code must be 5 digits.")

        if not errors:
            # Nothing is saved on purpose test only.
            flash("Account created! (Test only - nothing was saved.)")
            return redirect(url_for("login"))
    return render_template("signup.html", errors=errors, form=form)

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