import os
from datetime import timedelta

import cloudinary
from dotenv import load_dotenv
from flask import (
    Flask,
    Response,
    abort,
    current_app,
    redirect,
    render_template,
    request,
    send_from_directory,
    session,
    url_for,
)
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_session import Session
from flask_wtf.csrf import CSRFError, CSRFProtect

from database.db import database
from services.auth import *
from services.config import initialise_env
from services.validators import input_validator

load_dotenv()

initialise_env()

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ventory.db"
database.init_app(app)

from database.models import *

with app.app_context():
    database.create_all()

app.config["TEMPLATES_AUTO_RELOAD"] = True

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_SAMESITE="LAX",
    PERMANENT_SESSION_LIFETIME=timedelta(hours=1),
)

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True,
)


app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

Session(app)

csrf = CSRFProtect(app)

limiter = Limiter(key_func=get_remote_address, app=app)


@app.after_request
def security_headers(response):
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self'; "
        "style-src 'self' https://fonts.googleapis.com; "
        "font-src 'self' https://fonts.gstatic.com;"
    )
    return response


@app.route("/", methods=["GET", "POST"])
@limiter.limit("2 per hour; 10 per day", methods=["POST"])
def home_page():
    title = "Online Stock Management System"
    if request.method == "POST":
        return render_template("pages/main/confirm.html", title="Demo Only")
    return render_template("pages/main/home.html", title=title)


@app.route("/about-ventory")
def about_page():
    title = "SME Inventory System"
    return render_template("pages/main/about.html", title=title)


@app.route("/login", methods=["GET", "POST"])
@limiter.limit("5 per minute; 50 per day", methods=["POST"])
def login_page():
    if session.get("user-id"):
        return redirect(url_for(""))
    title = "Login to get started"
    return render_template("pages/main/login.html", title=title)


@app.route("/register", methods=["GET", "POST"])
@limiter.limit("2 per minute; 50 per day", methods=["POST"])
def register_page():
    title = "Sign up to use VenTory"
    error = ""
    if request.method == "POST":
        bname = request.form.get("business-name", "").strip().lower()
        bAddress = request.form.get("business-address", "").strip().lower()
        bemail = request.form.get("business-email", "").strip().lower()
        title = request.form.get("title", "").strip().lower()
        fname = request.form.get("fname", "").strip().lower()
        sname = request.form.get("sname", "").strip().lower()
        email = request.form.get("email", "").strip().lower()
        role = request.form.get("role", "").strip().lower()
        password = request.form.get("password", "").strip()
        confirm = request.form.get("confirm-password", "").strip()

        business = {
            "name": bname,
            "address": bAddress,
            "email": bemail,
            "daily_password": update_daily_password(),
        }

        user = {
            "title": title,
            "fname": fname,
            "sname": sname,
            "email": email,
            "role": role,
            "password": password,
            "confirm": confirm,
        }

        new_registration = {
            "business": business,
            "user": user,
        }

        success, error = input_validator(new_registration, "new business")

        if not success:
            return redirect(url_for("register_page", form_error=error))
    return render_template("pages/main/register.html", title=title, form_error=error)


@app.route("/robots.txt")
def robots():
    if current_app.static_folder is None:
        abort(404)
    return send_from_directory(current_app.static_folder, "robots.txt")


## change these:
@app.route("/sitemap.xml")
def sitemap():
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
    <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>{request.url_root}</loc>
    </url>
    <url>
        <loc>{request.url_root}about</loc>
    </url>
    <url>
        <loc>{request.url_root}login</loc>
    </url>
    <url>
        <loc>{request.url_root}register</loc>
    </url>
    </urlset>
    """
    return Response(xml, mimetype="application/xml")


@app.errorhandler(CSRFError)
def csrf_error(error):
    return render_template("pages/error/400.html", reason=error.description), 400


@app.errorhandler(403)
def forbidden(error):
    return render_template("pages/error/403.html"), 403


@app.errorhandler(404)
def not_found(error):
    return render_template("pages/error/404.html"), 404


@app.errorhandler(400)
def bad_request(error):
    return render_template("pages/error/400.html"), 400


@app.errorhandler(405)
def not_allowed(error):
    return render_template("pages/error/405.html"), 405


@app.errorhandler(500)
def server_error(error):
    return render_template("pages/error/500.html"), 500


@app.errorhandler(429)
def max_requests(error):
    return render_template("pages/error/429.html"), 429


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
