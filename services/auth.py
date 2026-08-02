import random
from datetime import datetime
from functools import wraps

from argon2 import PasswordHasher
from flask import redirect, session, url_for

hasher = PasswordHasher().hash
verifier = PasswordHasher().verify


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user-id") is None:
            return redirect(url_for("login"))
        return f(*args, **kwargs)

    return decorated_function


def update_daily_password():
    characters = "aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ0123456789"
    password = []
    for i in range(10):
        password.append(random.choice(characters))
    daily = "".join(password)
    return str(daily)


def generate_user_name():
    characters = "aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ0123456789"
    username = []
    for i in range(9):
        username.append(random.choice(characters))
    username = "".join(username)
    return str(username)

def generate_password_hash(password):
    hashed = hasher(password)
    return hashed


def generate_time():
    date = datetime.now().replace(microsecond=0).date()
    time = datetime.now().replace(microsecond=0).time()
    if str(time) > "12:00":
        suffix = "PM"
    else:
        suffix = "AM"
    return f"{date} {time} {suffix}"
