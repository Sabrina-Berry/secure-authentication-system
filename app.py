from flask import Flask, render_template, request, redirect, url_for, flash, session
from database import create_table, register_user, authenticate_user
from functools import wraps
from flask_wtf.csrf import CSRFProtect
import os
from dotenv import load_dotenv
import re

load_dotenv()

app = Flask(__name__)

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_SECURE"] = False

csrf = CSRFProtect(app)

# Create database table
create_table()
def validate_username(username):
    if len(username) < 3 or len(username) > 20:
        return False

    if not re.fullmatch(r"[A-Za-z0-9_]+", username):
        return False

    return True
def validate_email(email):
    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

    return re.fullmatch(pattern, email) is not None
def validate_password(password):
    if len(password) < 8:
        return False

    if not re.search(r"[A-Z]", password):
        return False

    if not re.search(r"[a-z]", password):
        return False

    if not re.search(r"[0-9]", password):
        return False

    return True

# Protect dashboard from unauthenticated users
def login_required(route):
    @wraps(route)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in first.")
            return redirect(url_for("login"))
        return route(*args, **kwargs)
    return wrapper


# Home page
@app.route("/")
def home():
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


# Registration
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        if not username or not email or not password:
            flash("All fields are required.")
            return redirect(url_for("register"))

        if not validate_username(username):
            flash("Username must be 3-20 characters and contain only letters, numbers or underscores.")
            return redirect(url_for("register"))

        if not validate_email(email):
            flash("Please enter a valid email address.")
            return redirect(url_for("register"))

        if not validate_password(password):
            flash("Password must contain at least 8 characters, one uppercase letter, one lowercase letter and one number.")
            return redirect(url_for("register"))

        success = register_user(username, email, password)

        if success:
            flash("Registration successful! Please log in.")
            return redirect(url_for("login"))

        flash("Username or email already exists.")

    return render_template("register.html")


# Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        user = authenticate_user(username, password)

        if user:
            session.clear()
            session["user_id"] = user["id"]
            session["username"] = user["username"]

            return redirect(url_for("dashboard"))

        flash("Invalid username or password.")

    return render_template("login.html")


# Dashboard
@app.route("/dashboard")
@login_required
def dashboard():
    return render_template(
        "dashboard.html",
        username=session["username"]
    )


# Logout
@app.route("/logout")
@login_required
def logout():
    session.clear()
    flash("You have been logged out.")
    return redirect(url_for("login"))


if __name__ == "__main__":
    if not app.secret_key:
        raise RuntimeError("SECRET_KEY is missing from .env")

    app.run(debug=True)
