from argon2 import PasswordHasher
from flask import session, redirect, url_for
from functools import wraps
from datetime import datetime, timedelta

hasher = PasswordHasher().hash
verifier = PasswordHasher().verify


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user-id") is None:
            return redirect(url_for("login"))
        return f(*args, **kwargs)

    return decorated_function


def create_new_user(user):
    date = datetime.now().replace(microsecond=0).date()
    time = datetime.now().replace(microsecond=0).time()
    username = user["username"]
    first_name = user["fname"]
    last_name = user["sname"]
    password = hasher(user["password"])
    created = f"{date} | {time}"

def login_user(user):
    


def update_daily_password():
    characters = "aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ0123456789"
    password = []
    for i in range(10):
        password.append(random.choice(characters))
    daily = "".join(password)
    return str(daily)
