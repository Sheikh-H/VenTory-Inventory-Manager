import os
from datetime import timedelta

import cloudinary

# import cloudinary.uploader
from dotenv import load_dotenv
from flask import (
    Flask,
    Response,
    abort,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    send_from_directory,
    session,
    url_for,
)
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_wtf.csrf import CSRFError, CSRFProtect
from sqlalchemy import true
from services.validators import input_validator

from database.db import database
from flask_session import Session
from services.auth import *
from services.businesses import *
from services.config import initialise_env

load_dotenv()

initialise_env()

app = Flask(__name__)


app.config.update(
    SECRET_KEY=os.getenv("SECRET_KEY"),
    SQLALCHEMY_DATABASE_URI="sqlite:///ventory.db",
    SESSION_TYPE="filesystem",
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_SAMESITE="LAX",
    PERMANENT_SESSION_LIFETIME=timedelta(hours=1),
    TEMPLATES_AUTO_RELOAD=True,
)


cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True,
)

database.init_app(app)

Session(app)

from database.models import Business, User, Stock, Log

with app.app_context():
    database.create_all()

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
    if session.get("user_id"):
        return redirect(url_for("dashboard"))
    title = "Login to get started"
    return render_template("pages/main/login.html", title=title)


@app.route("/register", methods=["GET", "POST"])
@limiter.limit("2 per minute; 50 per day", methods=["POST"])
def register_page():
    title = "Sign up to use VenTory"
    if session.get("user_id"):
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        bName = request.form.get("business-name", "").strip().lower()
        if len(bName) < 5:
            bName = ""
        if bName:
            valid_business_name = input_validator(bName, "text")
            if not valid_business_name:
                bName = ""
        bAddress = request.form.get("business-address", "").strip().lower()
        if len(bAddress) < 30:
            bAddress = ""
        if bAddress:
            valid_address = input_validator(bAddress, "text")
            if not valid_address:
                bAddress = ""
        bTelephone = request.form.get("business-telepone", "").strip().lower()
        if len(bTelephone) < 10 or len(bTelephone) > 15:
            bTelephone = ""
        if bTelephone:
            valid_telephone = input_validator(bTelephone, "telephone")
            if not valid_telephone:
                bTelephone = ""

        bEmail = request.form.get("business-email", "").strip().lower()
        uEmail = request.form.get("email", "").strip().lower()
        if bEmail:
            valid_email = input_validator(bEmail, "email")
            if not valid_email:
                bEmail = ""
        if uEmail:
            valid_email = input_validator(uEmail, "email")
            if not valid_email:
                uEmail = ""
        if uEmail == bEmail:
            uEmail = ""
            bEmail = ""
        bTitle = request.form.get("title", "").strip().lower()
        if bTitle not in ["dr", "mr", "mrs", "miss", "ms"]:
            bTitle = ""
        fname = request.form.get("first-name", "").strip().lower()
        if len(fname) < 1 or len(fname) > 100:
            fname = ""
        if fname:
            valid_fname = input_validator(fname, "text")
            if not valid_fname:
                fname = ""
        sname = request.form.get("last-name", "").strip().lower()
        if len(sname) < 1 or len(sname) > 100:
            sname = ""
        if sname:
            valid_sname = input_validator(sname, "text")
            if not valid_sname:
                sname = ""
        role = request.form.get("role", "").strip().lower()
        if role not in ["owner", "employee", "manager"]:
            role = ""
        password = request.form.get("password", "").strip()
        if len(password) < 15 or len(password) > 25:
            password = ""
        if password:
            valid_password = input_validator(password, "text")
            if not valid_password:
                password = ""
        confirm_password = request.form.get("confirm-password", "").strip()
        if len(confirm_password) < 15 or len(confirm_password) > 25:
            confirm_password = ""
        if confirm_password:
            valid_confirm = input_validator(confirm_password, "text")
            if not valid_confirm:
                confirm_password = ""
        if password != confirm_password:
            password = ""
            confirm_password = ""
        data = {
            "name": bName,
            "address": bAddress,
            "telephone": bTelephone,
            "bemail": bEmail,
            "title": bTitle,
            "fname": fname,
            "sname": sname,
            "uemail": uEmail,
            "role": role,
            "password": confirm_password,
        }
        user_id = new_business_registration(data)
        if user_id:
            session.clear()
            session.permanent = True
            session["user_id"] = user_id
            return redirect(url_for("dashboard"))
        flash("Unable to validate inputs, please try again!", "error")

    return render_template("pages/main/register.html", title=title)


@app.route("/user/dashboard/", methods=["GET", "POST"])
@login_required
def dashboard():
    user = User.query.filter_by(user_id=session.get("user_id")).first()
    business = Business.query.filter_by(business_id=user.business_id).first()
    session["role"] = user.role
    session["user-id"] = user.user_id
    session["business-id"] = business.business_id
    title = f"{business.name}"
    username = user.username
    return render_template(
        "pages/user-pages/dashboard.html", title=title, username=username
    )


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
