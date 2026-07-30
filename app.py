from flask import (
    Flask,
    url_for,
    render_template,
    Response,
    request,
    current_app,
    send_from_directory,
    abort,
)
from flask_wtf.csrf import CSRFProtect, CSRFError
from datetime import timedelta, datetime
from flask_session import Session
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_SAMESITE="LAX",
    PERMANENT_SESSION_LIFETIME=timedelta(hours=1),
)

app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

Session(app)

csrf = CSRFProtect(app)


@app.route("/")
def home_page():
    title = "Online Stock Management System"
    return render_template("pages/main/home.html", title=title)


@app.route("/about-ventory")
def about_page():
    title = "SME Inventory System"
    return render_template("pages/main/about.html", title=title)


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


@app.errorhandler(500)
def server_error(error):
    return render_template("pages/error/500.html"), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
