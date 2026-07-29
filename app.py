from flask import Flask, url_for, render_template
import os

app = Flask(__name__)


@app.route("/")
def home_page():
    return render_template("pages/main/home.html")


if __name__ == "__main__":
    port = os.environ.get("PORT", 5000)
    app.run(debug=True, host="0.0.0.0", port=port)
