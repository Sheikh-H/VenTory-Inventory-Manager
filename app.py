import os
from datetime import timedelta

import cloudinary
import cloudinary.uploader
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
from flask_session import Session
from flask_wtf.csrf import CSRFError, CSRFProtect

from database.db import database
from services.auth import *
from services.businesses import *
from services.config import *
from services.users import *
from services.validators import *

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

from database.models import *

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
        "img-src 'self' https://placehold.co https://res.cloudinary.com/dcnpmdfzl/image/upload/;"
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
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        valid_username = input_validator(username, "text")
        if not valid_username:
            username = ""
        valid_password = input_validator(password, "text")
        if not valid_password:
            password = ""
        success, user_id = login_user(username, password)
        if success:
            session.clear()
            session.permanent = True
            session["user_id"] = user_id
            flash("Logged in!", "success")
            return redirect(url_for("dashboard"))
        return redirect(url_for("login_page"))
    return render_template("pages/main/login.html", title=title)


@app.route("/register", methods=["GET", "POST"])
@limiter.limit("2 per minute; 50 per day", methods=["POST"])
def register_page():
    title = "Sign up to use VenTory"
    if session.get("user_id"):
        return redirect(url_for("dashboard"))
    if request.method == "POST":
        bName = request.form.get("business-name", "").strip().lower()
        if len(bName) < 5 or len(bName) > 255:
            bName = ""
        if bName:
            valid_business_name = input_validator(bName, "text")
            if not valid_business_name:
                bName = ""
        bAddress = request.form.get("business-address", "").strip().lower()
        if len(bAddress) < 30 or len(bAddress) > 255:
            bAddress = ""
        if bAddress:
            valid_address = input_validator(bAddress, "text")
            if not valid_address:
                bAddress = ""
        bTelephone = request.form.get("business-telephone", "").strip().lower()
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
        fname = request.form.get("fname", "").strip().lower()
        if len(fname) < 1 or len(fname) > 100:
            fname = ""
        if fname:
            valid_fname = input_validator(fname, "text")
            if not valid_fname:
                fname = ""
        sname = request.form.get("sname", "").strip().lower()
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
        if len(password) < 10 or len(password) > 20:
            password = ""
        if password:
            valid_password = input_validator(password, "text")
            if not valid_password:
                password = ""
        confirm_password = request.form.get("confirm-password", "").strip()
        if len(confirm_password) < 10 or len(confirm_password) > 20:
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
    return render_template("pages/main/register.html", title=title)


@app.route("/user/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    title = "Welcome to your dashboard"
    user = User.query.filter_by(user_id=session.get("user_id")).first()
    new_user = bool(
        user.created[0:10] == str(datetime.now().replace(microsecond=0).date())
    )
    business = Business.query.filter_by(business_id=user.business_id).first()
    session["role"] = user.role
    session["user-id"] = user.user_id
    session["business-id"] = business.business_id
    return render_template(
        "pages/user-pages/dashboard.html",
        title=title,
        user=user,
        new_user=new_user,
        business=business,
    )


@app.route("/user/owner-settings", methods=["GET", "POST"])
@login_required
@limiter.limit("3 per day", methods=["POST"])
def owner_settings():
    title = "Update your details"
    user = User.query.filter_by(user_id=session.get("user_id")).first()
    if user.role != "owner":
        return redirect(url_for("user_settings"))
    business = Business.query.filter_by(business_id=user.business_id).first()
    if request.method == "POST":
        bName = request.form.get("business-name", "").strip().lower()
        if len(bName) < 5 or len(bName) > 255:
            bName = ""
        if bName:
            valid_business_name = input_validator(bName, "text")
            if not valid_business_name:
                bName = ""
        bAddress = request.form.get("business-address", "").strip().lower()
        if len(bAddress) < 30 or len(bAddress) > 255:
            bAddress = ""
        if bAddress:
            valid_address = input_validator(bAddress, "text")
            if not valid_address:
                bAddress = ""
        bTelephone = request.form.get("business-telephone", "").strip().lower()
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
        fname = request.form.get("fname", "").strip().lower()
        if len(fname) < 1 or len(fname) > 100:
            fname = ""
        if fname:
            valid_fname = input_validator(fname, "text")
            if not valid_fname:
                fname = ""
        sname = request.form.get("sname", "").strip().lower()
        if len(sname) < 1 or len(sname) > 100:
            sname = ""
        if sname:
            valid_sname = input_validator(sname, "text")
            if not valid_sname:
                sname = ""
        password = request.form.get("password", "").strip()
        if len(password) < 10 or len(password) > 20:
            password = ""
        if password:
            valid_password = input_validator(password, "text")
            if not valid_password:
                password = ""
        image = request.files.get("image")
        if not image:
            image = ""
            image_url = None
        if image:
            try:
                upload = cloudinary.uploader.upload(
                    image, folder=f"{business.business_name}"
                )
                image_url = upload["secure_url"]
            except Exception as e:
                print(e)
        data = {
            "user_id": user.user_id,
            "business_id": user.business_id,
            "name": bName,
            "address": bAddress,
            "telephone": bTelephone,
            "image_url": image_url,
            "bemail": bEmail,
            "title": bTitle,
            "fname": fname,
            "sname": sname,
            "uemail": uEmail,
            "password": password,
        }
        success = update_details(data, "owner")
        if success:
            flash("Details have been updated successfully!", "success")
            return redirect(url_for("dashboard"))
        flash("Unable to update, contact admin!", "error")
        return redirect(url_for("dashboard"))
    return render_template(
        "pages/user-pages/account-settings.html",
        title=title,
        user=user,
        business=business,
    )


@app.route("/user/user-settings", methods=["GET", "POST"])
@login_required
@limiter.limit("3 per day", methods=["POST"])
def user_settings():
    title = "Update your details"
    user = User.query.filter_by(user_id=session.get("user_id")).first()
    if user.role == "owner":
        return redirect(url_for("owner_settings"))
    if request.method == "POST":
        uEmail = request.form.get("email", "").strip().lower()
        if uEmail:
            valid_email = input_validator(uEmail, "email")
            if not valid_email:
                uEmail = ""
        bTitle = request.form.get("title", "").strip().lower()
        if bTitle not in ["dr", "mr", "mrs", "miss", "ms"]:
            bTitle = ""
        fname = request.form.get("fname", "").strip().lower()
        if len(fname) < 1 or len(fname) > 100:
            fname = ""
        if fname:
            valid_fname = input_validator(fname, "text")
            if not valid_fname:
                fname = ""
        sname = request.form.get("sname", "").strip().lower()
        if len(sname) < 1 or len(sname) > 100:
            sname = ""
        if sname:
            valid_sname = input_validator(sname, "text")
            if not valid_sname:
                sname = ""
        password = request.form.get("password", "").strip()
        if len(password) < 10 or len(password) > 20:
            password = ""
        if password:
            valid_password = input_validator(password, "text")
            if not valid_password:
                password = ""
        data = {
            "user_id": user.user_id,
            "business_id": user.business_id,
            "title": bTitle,
            "fname": fname,
            "sname": sname,
            "uemail": uEmail,
            "password": password,
        }
        success = update_details(data, "user")
        if success:
            flash("Details updated successfully!", "success")
            return redirect(url_for("dashboard"))
        flash("Unable to update, contact admin!", "error")
        return redirect(url_for("dashboard"))
    return render_template(
        "pages/user-pages/account-settings.html",
        title=title,
        user=user,
    )


@app.route("/user/update-password", methods=["POST"])
@login_required
@limiter.limit("3 per day", methods=["POST"])
def update_password():
    user = User.query.filter_by(user_id=session.get("user_id")).first()
    current_password = request.form.get("current-password", "").strip()
    if not current_password:
        current_password = ""
    if len(current_password) < 10 or len(current_password) > 20:
        current_password = ""
    valid_password = input_validator(current_password, "text")
    if not valid_password:
        current_password = ""
    new_password = request.form.get("new-password", "").strip()
    if not new_password:
        new_password = ""
    if len(new_password) < 10 or len(new_password) > 20:
        new_password = ""
    valid_new_password = input_validator(new_password, "text")
    if not valid_new_password:
        new_password = ""
    confirm_new_password = request.form.get("confirm-new-password", "").strip()
    if not confirm_new_password:
        confirm_new_password = ""
    if len(confirm_new_password) < 10 or len(confirm_new_password) > 20:
        confirm_new_password = ""
    valid_confirm_password = input_validator(confirm_new_password, "text")
    if not valid_confirm_password:
        confirm_new_password = ""
    if confirm_new_password != new_password:
        new_password = ""
        confirm_new_password = ""
    success = password_update(user, new_password, current_password)
    if success:
        flash("Password updated successfully!", "success")
        return redirect(url_for("dashboard"))
    flash("Unable to update password!", "error")
    return redirect(url_for("dashboard"))


@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    user = User.query.filter_by(user_id=session.get("user_id")).first()
    business = Business.query.filter_by(business_id=user.business_id).first()
    generate_new_log(
        user.user_id, business.business_id, f"{user.first_name} logged out!"
    )
    session.clear()
    flash("Successfully logged out!", "success")
    return redirect(url_for("home_page"))


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
