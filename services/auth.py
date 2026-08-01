from flask import session, redirect, url_for
from datetime import datetime, timedelta
from argon2 import PasswordHasher
from functools import wraps
import random

hasher = PasswordHasher().hash
verifier = PasswordHasher().verify


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user-id") is None:
            return redirect(url_for("login"))
        return f(*args, **kwargs)

    return decorated_function


def create_new_user(data):
    business_id = create_new_business(data)
    
    username = []

    for _ in range(9):
        username.append(random.randint(0, 9))

    data["username"] = "".join(username)

    if data["password"] == data["confirm"]:
        data["password"] = hasher(data["confirm"])

    data.discard("confirm")


def login_user(user):
    return


def update_daily_password():
    characters = "aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ0123456789"
    password = []
    for i in range(10):
        password.append(random.choice(characters))
    daily = "".join(password)
    return str(daily)


def generate_time():
    date = datetime.now().replace(microsecond=0).date()
    time = datetime.now().replace(microsecond=0).time()

    if str(time) > "12:00":
        suffix = "PM"
    else:
        suffix = "AM"

    return f"{date} {time} {suffix}"


def update_log(date, action, user, business):
    entry = f"{date} | {user} {action}"
    return


def create_new_business(business):
    # for business in businesses 
        # if business name in the list,
            # if business email in the list
                # if business address in the list
                    # if business telephone in list
                        # reject entry
        
    return
