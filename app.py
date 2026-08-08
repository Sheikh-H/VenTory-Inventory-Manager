import os
from datetime import timedelta

import cloudinary
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
from sqlalchemy import or_

from database.db import database
from flask_session import Session
from services.auth import *
from services.businesses import *
from services.config import *
from services.stock import *
from services.users import *
from services.validators import *

load_dotenv()

initialise_env()

load_dotenv()

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
        "img-src 'self' https://placehold.co "
        "https://res.cloudinary.com/dcnpmdfzl/image/upload/;"
    )
    return response


@app.route("/", methods=["GET", "POST"])
@limiter.limit("2 per hour; 10 per day", methods=["POST"])
def home_page():
    title = "Online Stock Management System"
    update_daily_password()
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
        success, user_id = login_user(username, password)
        if success:
            session.clear()
            session.permanent = True
            session["user_id"] = user_id
            flash("Logged in!", "success")
            return redirect(url_for("dashboard"))
        flash("Unable to login!", "error")
        return redirect(url_for("login_page"))
    return render_template("pages/main/login.html", title=title)


@app.route("/register", methods=["GET", "POST"])
@limiter.limit("3 per minute; 10 per day", methods=["POST"])
def register_page():
    title = "Sign up to use VenTory"
    if session.get("user_id"):
        return redirect(url_for("dashboard"))
    if request.method == "POST":
        bName = request.form.get("business-name", "").strip().lower()
        bAddress = request.form.get("business-address", "").strip().lower()
        bTelephone = request.form.get("business-telephone", "").strip().lower()
        bEmail = request.form.get("business-email", "").strip().lower()
        uTitle = request.form.get("title", "").strip().lower()
        fname = request.form.get("fname", "").strip().lower()
        sname = request.form.get("sname", "").strip().lower()
        uEmail = request.form.get("email", "").strip().lower()
        role = request.form.get("role", "").strip().lower()
        password = request.form.get("password", "").strip()
        confirm_password = request.form.get("confirm-password", "").strip()
        if role not in ["owner", "employee", "manager"]:
            role = ""
        if role != "owner":
            flash("Please ask the owner of the business to register!", "error")
            return redirect(url_for("register_page"))
        if password != confirm_password:
            flash("Passwords don't match, try again!", "error")
            return redirect(url_for("register_page"))
        if uEmail == bEmail:
            flash("Please use different email address for business and user", "error")
            return redirect(url_for("register_page"))
        data = {
            "name": bName,
            "address": bAddress,
            "telephone": bTelephone,
            "bemail": bEmail,
            "title": uTitle,
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
            flash("Username generated, please keep a copy of this to login!", "success")
            return redirect(url_for("dashboard"))
        flash("Unable to register new account, try again!", "error")
        return redirect(url_for("register_page"))
    return render_template("pages/main/register.html", title=title)


@app.route("/user/log/<int:emp_id>", methods=["GET"])
@login_required
@owner_required
def employee_logs(emp_id):
    emp = User.query.filter_by(
        user_id=emp_id, business_id=session.get("business_id")
    ).first()
    if not emp:
        flash("Employee not found!", "error")
        return redirect(url_for("manage_employees"))
    title = f"All logs for {emp.username}"
    logs = Log.query.filter_by(user_id=emp.user_id, business_id=emp.business_id).all()
    return render_template(
        "pages/user-pages/manager/employee-log.html", logs=logs, title=title, emp=emp
    )


@app.route("/user/business-activity", methods=["GET", "POST"])
@login_required
@owner_required
def business_logs():
    title = "Business Activity"
    logs = (
        Log.query.filter_by(business_id=session.get("business_id"))
        .order_by(Log.timestamp.desc())
        .all()
    )
    now = str(datetime.now().replace(microsecond=0).date())
    if request.method == "POST":
        date = request.form.get("date", "").strip()
        valid_date = input_validator(date, "date")
        if not valid_date:
            flash("Incorrect date format!", "error")
            return redirect(url_for("business_logs"))
        logs = (
            Log.query.filter(
                Log.business_id == session.get("business_id"),
                Log.timestamp >= f"{valid_date} 00:00:00",
                Log.timestamp <= f"{valid_date} 23:59:59",
            )
            .order_by(Log.timestamp.desc())
            .all()
        )
        return render_template(
            "pages/user-pages/owner/all-logs.html",
            title=title,
            logs=logs,
            now=now,
        )
    return render_template(
        "pages/user-pages/owner/all-logs.html", title=title, logs=logs, now=now
    )


@app.route("/forgotten-password", methods=["GET", "POST"])
@limiter.limit("3 per minute; 6 per day", methods=["POST"])
def forgotten_password():
    title = "Forgot Password"
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        daily_password = request.form.get("password", "").strip()
        data = {"username": username, "password": daily_password}
        success, user_id = forgot_password(data)
        if success:
            flash("Password reset, please change your password on login!", "success")
            session["user_id"] = user_id
            return redirect(url_for("dashboard"))
        else:
            flash("Unable to reset, please contact your manager!", "error")
            return redirect(url_for("forgotten_password"))
    return render_template("pages/main/forgotten_password.html", title=title)


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
    session["business_id"] = business.business_id
    user = User.query.filter_by(
        user_id=session.get("user_id"), business_id=session.get("business_id")
    ).first()
    total_stock = 0
    total_price = 0.00
    total_returned = 0
    total_return_price = 0.00
    total_damaged = 0
    total_damage_price = 0.00
    if user.role in ["manager", "owner"]:
        all_stocks = Stock.query.filter_by(business_id=user.business_id).all()
        for stock in all_stocks:
            total_stock += stock.available
            total_stock += stock.returned
            total_price += stock.price * stock.available
            total_returned += stock.returned
            total_return_price += (stock.price / 2) * stock.returned
            total_damaged += stock.damaged
            total_damage_price += stock.price * stock.damaged
        total_price += total_return_price
    if user.password_reset == 1:
        flash(
            "Your password was reset by an admin user, please reset your password!",
            "error",
        )
        return redirect(url_for("account_settings"))
    return render_template(
        "pages/user-pages/dashboard.html",
        title=title,
        user=user,
        new_user=new_user,
        business=business,
        total_stock=total_stock,
        total_price=total_price,
        total_returned=total_returned,
        total_damaged=total_damaged,
        total_return_price=total_return_price,
        total_damage_price=total_damage_price,
    )


@app.route("/user/account-settings", methods=["GET"])
@login_required
def account_settings():
    title = "Update account details"
    user = User.query.filter_by(
        user_id=session.get("user_id"), business_id=session.get("business_id")
    ).first()
    business = Business.query.filter_by(business_id=user.business_id).first()
    return render_template(
        "pages/user-pages/account-settings.html",
        title=title,
        user=user,
        business=business,
    )


@app.route("/user/update-details", methods=["POST"])
@login_required
@limiter.limit("2 per day")
def update():
    user = User.query.filter_by(
        user_id=session.get("user_id"), business_id=session.get("business_id")
    ).first()
    business = Business.query.filter_by(business_id=user.business_id).first()
    business_name = request.form.get("business-name", "").strip().lower()
    business_address = request.form.get("business-address", "").strip().lower()
    business_telephone = request.form.get("business-telephone", "").strip()
    business_email = request.form.get("business-email", "").strip().lower()
    user_title = request.form.get("title", "").strip().lower()
    user_first_name = request.form.get("fname", "").strip().lower()
    user_last_name = request.form.get("sname", "").strip().lower()
    user_email = request.form.get("email", "").strip().lower()
    user_password = request.form.get("password", "").strip()
    image = request.files.get("image")
    image_url = image_upload(image, "logo", business.business_name)
    data = {
        "user_id": user.user_id,
        "business_id": user.business_id,
        "bname": business_name,
        "address": business_address,
        "telephone": business_telephone,
        "image_url": image_url,
        "bemail": business_email,
        "title": user_title,
        "fname": user_first_name,
        "sname": user_last_name,
        "uemail": user_email,
        "password": user_password,
    }
    success = update_details(data)
    if success:
        flash("Details updated!", "success")
        return redirect(url_for("dashboard"))
    flash("Unable to update the details!", "error")
    return redirect(url_for("update"))


@app.route("/user/update-password", methods=["POST"])
@login_required
@limiter.limit("2 per day", methods=["POST"])
def update_password():
    user = User.query.filter_by(
        user_id=session.get("user_id"), business_id=session.get("business_id")
    ).first()
    current_password = request.form.get("current-password", "").strip()
    new_password = request.form.get("new-password", "").strip()
    confirm_new_password = request.form.get("confirm-new-password", "").strip()
    if new_password != confirm_new_password:
        flash("Passwords don't match, try again!", "error")
        return redirect(url_for("update_password"))
    success = password_update(user, confirm_new_password, current_password)
    if success:
        flash("Password updated successfully!", "success")
        return redirect(url_for("dashboard"))
    else:
        flash("Unable to update password!", "error")
        return redirect(url_for("update_password"))


@app.route("/user/add-new-stock", methods=["GET", "POST"])
@login_required
def add_stock():
    title = "Add new stock"
    user = User.query.filter_by(user_id=session.get("user_id")).first()
    if request.method == "POST":
        image = request.files.get("image", None)
        product_title = request.form.get("title", "").strip().lower()
        quantity = request.form.get("quantity", "")
        supplier = request.form.get("supplier", "").strip().lower()
        additional_info = request.form.get("description", "").strip().lower()
        price = request.form.get("price", "")
        stock = {
            "user_id": user.user_id,
            "business_id": user.business_id,
            "title": product_title,
            "image": image,
            "description": additional_info,
            "quantity": quantity,
            "supplier": supplier,
            "price": price,
        }
        success = add_new_stock(stock, user)
        if success:
            flash("Stock added successfully!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Unable to add stock!", "error")
            return redirect(url_for("add_stock"))
    return render_template("pages/user-pages/add-new-stock.html", title=title)


@app.route("/user/add-employee", methods=["GET", "POST"])
@login_required
@owner_required
@limiter.limit("5 per day", methods=["POST"])
def add_employee():
    title = "Add new employee"
    user = User.query.filter_by(user_id=session.get("user_id")).first()
    if "generated_password" not in session:
        session["generated_password"] = generate_daily_password()
    if "generated_username" not in session:
        session["generated_username"] = generate_user_name()
    if request.method == "POST":
        data = {
            "admin_id": user.user_id,
            "business_id": user.business_id,
            "username": session["generated_username"],
            "title": request.form.get("title", "").strip().lower(),
            "fname": request.form.get("fname", "").strip().lower(),
            "sname": request.form.get("sname", "").strip().lower(),
            "email": request.form.get("email", "").strip().lower(),
            "role": request.form.get("role", "").strip().lower(),
            "password": session["generated_password"],
        }
        success = add_new_user(data)
        if success:
            session.pop("generated_password", None)
            session.pop("generated_username", None)
            flash("New user added!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Unable to add new user!", "error")
            return redirect(url_for("add_employee"))
    return render_template(
        "pages/user-pages/owner/add-employee.html",
        title=title,
        generated_password=session["generated_password"],
        generated_username=session["generated_username"],
    )


@app.route("/user/manage-employees", methods=["GET", "POST"])
@login_required
@owner_required
def manage_employees():
    title = "Manage Employees"
    user = User.query.filter_by(user_id=session.get("user_id")).first()
    business = Business.query.filter_by(business_id=user.business_id).first()
    users = User.query.filter(
        User.business_id == business.business_id, User.role.in_(["manager", "employee"])
    ).all()
    if request.method == "POST":
        search = request.form.get("search", "").strip().lower()
        valid_search = input_validator(search, "text", maximum=255)
        if valid_search:
            users = User.query.filter(
                User.business_id == business.business_id,
                User.role.in_(["manager", "employee"]),
                or_(
                    User.last_name.ilike(f"%{valid_search}%"),
                    User.first_name.ilike(f"%{valid_search}%"),
                    User.username.ilike(f"%{valid_search}%"),
                ),
            ).all()
            return render_template(
                "/pages/user-pages/manager/manage-employee.html",
                title=title,
                users=users,
            )
    return render_template(
        "/pages/user-pages/manager/manage-employee.html", title=title, users=users
    )


@app.route("/user/employee/<int:emp_id>", methods=["GET", "POST"])
@login_required
@owner_required
def employee(emp_id):
    user = User.query.filter_by(user_id=session.get("user_id")).first()
    employee = User.query.filter(user_id=emp_id, business_id=user.business_id).first()
    if not employee:
        flash("Employee not found!", "error")
        return redirect(url_for("manage_employees"))
    title = f"{employee.username}"
    return render_template(
        "/pages/user-pages/manager/employee-page.html", title=title, employee=employee
    )


@app.route("/user/delete-employee/<int:emp_id>", methods=["POST"])
@login_required
@owner_required
@limiter.limit("10 per day", methods=["POST"])
def delete_employee(emp_id):
    user = User.query.filter_by(
        user_id=session.get("user_id"), business_id=session.get("business_id")
    ).first()
    data = {
        "user_id": user.user_id,
        "business_id": user.business_id,
        "delete_id": emp_id,
    }
    success = remove_user(data)
    if success:
        flash("Employee has been deleted!", "success")
        return redirect(url_for("manage_employees"))

    else:
        flash("Unable to delete employee, try again!", "error")
        return redirect(url_for("employee", emp_id=emp_id))


@app.route("/user/password-reset/<int:emp_id>", methods=["POST"])
@login_required
@manager_required
@limiter.limit("5 per day", methods=["POST"])
def reset(emp_id):
    date = generate_time()
    admin = User.query.filter_by(
        user_id=session.get("user_id"), business_id=session.get("business_id")
    ).first()
    user = User.query.filter_by(user_id=emp_id, business_id=admin.business_id).first()

    password = generate_daily_password()
    hashed = generate_password_hash(password)
    try:
        user.password = hashed
        user.updated = date
        user.password_reset = 1
        database.session.commit()
        generate_new_log(
            admin.user_id,
            admin.business_id,
            f"{admin.first_name} Did a password reset for {user.username} : {user.first_name}",
        )
        flash("Password reset for user!", "success")
        return redirect(url_for("employee", emp_id=emp_id))
    except Exception as e:
        print(e)
        database.session.rollback()
        flash("Unable to reset password for user!", "error")
        return redirect(url_for("employee", emp_id=emp_id))


@app.route("/user/all-stock", methods=["GET", "POST"])
@login_required
def all_stock():
    title = "All stock"
    user = User.query.filter_by(user_id=session.get("user_id")).first()
    stocks = Stock.query.filter_by(business_id=user.business_id).all()
    if request.method == "POST":
        search = request.form.get("search", "").strip().lower()
        valid_search = input_validator(search, "text")
        stocks = Stock.query.filter(
            Stock.business_id == user.business_id,
            Stock.title.ilike(f"%{valid_search}%"),
        ).all()
        return render_template(
            "pages/user-pages/all-stock.html", title=title, stocks=stocks
        )
    return render_template(
        "pages/user-pages/all-stock.html", title=title, stocks=stocks
    )


@app.route("/user/stock/<int:stock_id>", methods=["GET", "POST"])
@login_required
def stock_page(stock_id):
    user = User.query.filter_by(user_id=session.get("user_id")).first()
    stock = Stock.query.filter_by(
        business_id=user.business_id, stock_id=stock_id
    ).first()
    if not stock:
        flash("Stock item not found.", "error")
        return redirect(url_for("all_stock"))
    title = f"{stock.title.title()}"
    if request.method == "POST":
        new_image = request.files.get("image")
        new_title = request.form.get("title", "").strip().lower()
        new_description = request.form.get("description", "").strip().lower()
        new_supplier = request.form.get("supplier", "").strip().lower()
        new_available = request.form.get("available", "").strip().lower()
        new_returned = request.form.get("returned", "").strip().lower()
        new_damaged = request.form.get("damaged", "").strip().lower()
        new_price = request.form.get("price", "").strip().lower()
        data = {
            "stock_id": stock_id,
            "business_id": user.business_id,
            "user_id": user.user_id,
            "image": new_image,
            "title": new_title,
            "description": new_description,
            "supplier": new_supplier,
            "available": new_available,
            "returned": new_returned,
            "damaged": new_damaged,
            "price": new_price,
        }
        success = update_stock(data)
        if success:
            flash("Stock updated successfully!", "success")
            return redirect(url_for("all_stock"))
        else:
            flash("Unable to update stock!", "error")
            return redirect(url_for("stock_page", stock_id=stock_id))
    return render_template("pages/user-pages/stock-page.html", title=title, stock=stock)


@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    user = User.query.filter_by(user_id=session.get("user_id")).first()
    business = Business.query.filter_by(business_id=user.business_id).first()
    generate_new_log(
        user.user_id, business.business_id, f"{user.first_name} logged out!"
    )
    update_daily_password()
    session.clear()
    flash("Successfully logged out!", "success")
    return redirect(url_for("home_page"))


@app.route("/user/delete-stock/<int:stock_id>", methods=["POST"])
@login_required
@manager_required
@limiter.limit("10 per day", methods=["POST"])
def delete_stock(stock_id):
    user = User.query.filter_by(user_id=session.get("user_id")).first()
    business = Business.query.filter_by(business_id=user.business_id).first()
    stock = Stock.query.filter_by(
        business_id=business.business_id, stock_id=stock_id
    ).first()
    if not stock:
        flash("Stock not found!", "error")
        return redirect(url_for("all_stock"))
    data = {
        "stock_id": stock.stock_id,
        "business_id": business.business_id,
        "user_id": user.user_id,
    }
    success = delete_item(data)
    if success:
        flash("Item has been deleted!", "success")
        return redirect(url_for("all_stock"))
    else:
        flash("Unable to delete stock item, try again!", "error")
        return redirect(url_for("stock_page", stock_id=stock_id))


@app.route("/robots.txt")
def robots():
    if current_app.static_folder is None:
        abort(404)
    return send_from_directory(current_app.static_folder, "robots.txt")


@app.route("/sitemap.xml")
def sitemap():
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
    <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>{request.url_root}</loc>
    </url>
    <url>
        <loc>{request.url_root}about-ventory</loc>
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
    app.run(debug=False, host="0.0.0.0", port=port)
