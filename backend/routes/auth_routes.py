from flask import Blueprint, request, redirect, render_template, url_for, flash
from backend.models.authentication import Authentication
import re
auth_bp = Blueprint("auth", __name__)
authentication = Authentication()

# Login
@auth_bp.route("/", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        email = request.form.get("email", "")
        password = request.form.get("password", "")

        if authentication.login(email, password):
            return redirect(url_for("main.main"))

        error = "Incorrect email or password."

    return render_template("login.html", error=error)

# Logout
@auth_bp.route("/logout", methods=["POST"]) # CHANGE to <form action="{{ url_for('auth.logout') }}" method="POST"> in front
def logout():
    authentication.logout()
    return redirect(url_for("auth.login"))

# Register
@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    errors = []

    fields = ["first_name", "last_name", "phone", "email"]
    form = {field: "" for field in fields}

    if request.method == "POST":
        form = {
            field: request.form.get(field, "").strip()
            for field in fields
        }

        password = request.form.get("password", "")
        confirm = request.form.get("confirm_password", "")

        # Validate form fields
        for field in fields:
            if not form[field]:
                errors.append(f"{field.replace('_', ' ').title()} is required.")

        if len(password) < 8:
            errors.append("Password must be at least 8 characters.")

        if password != confirm:
            errors.append("Passwords do not match.")

        if form["email"] and not re.fullmatch(
            r"[^@\s]+@[^@\s]+\.[^@\s]+", form["email"]
        ):
            errors.append("Enter a valid email address.")

        if form["phone"] and len(re.sub(r"\D", "", form["phone"])) != 10:
            errors.append("Phone number must have 10 digits.")

        # Register the customer if validation succeeds
        if not errors:
            success = authentication.register_customer(
                email=form["email"],
                password=password,
                fname=form["first_name"],
                lname=form["last_name"],
                phone_number=form["phone"]
            )

            if success:
                flash("Account created successfully! Please log in.")
                return redirect(url_for("auth.login"))

            errors.append("An account with that email already exists.")

    return render_template("signup.html", errors=errors, form=form)