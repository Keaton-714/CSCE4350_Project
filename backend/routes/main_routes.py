from flask import Blueprint, render_template, redirect, session, url_for, abort
from backend.database.connection import get_connection

main_bp = Blueprint("main", __name__)

@main_bp.route("/main")
def main():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    
    if session.get("account_type") != "customer":
        abort(403)

    connection = get_connection()

    try:
        user = connection.execute(
            "SELECT fname FROM User WHERE user_id = ?",
            (session["user_id"],)
        ).fetchone()
    finally:
        connection.close()

    if user is None:
        session.pop("user_id", None)
        return redirect(url_for("auth.login"))

    return render_template("main.html", user=user["fname"])

@main_bp.route("/main/employee")
def employee_main():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if session.get("account_type") != "employee":
        abort(403)

    return render_template("employee.html")