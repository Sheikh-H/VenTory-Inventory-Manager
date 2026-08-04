import random
from datetime import datetime
from functools import wraps

from argon2 import PasswordHasher
from flask import redirect, session, url_for

from database.db import database
from database.models import *
from services.config import *
from services.log import *

hasher = PasswordHasher().hash
verifier = PasswordHasher().verify


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect(url_for("login_page"))
        return f(*args, **kwargs)

    return decorated_function


def owner_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("role") != "owner":
            return redirect(url_for("dashboord"))
        return f(*args, **kwargs)

    return decorated_function


def generate_daily_password():
    characters = "aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ0123456789"
    password = []
    for i in range(10):
        password.append(random.choice(characters))
    daily = "".join(password)
    return str(daily)


def generate_user_name():
    characters = "aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ0123456789"
    new_username = []
    usernames = [
        username for (username,) in database.session.query(User.username).all()
    ]

    for i in range(9):
        new_username.append(random.choice(characters))

    new_username = "".join(new_username)

    for users in usernames:
        if new_username == users:
            return generate_user_name()
    return str(new_username)


def generate_password_hash(password):
    hashed = hasher(password)
    return hashed


def login_user(username, password):
    user = User.query.filter_by(username=username).first()
    update_daily_password()
    try:
        verifier(password=password, hash=user.password)
        generate_new_log(
            user.user_id, user.business_id, f"{user.first_name} logged in!"
        )
        return True, user.user_id
    except Exception as e:
        print(e)
        return False, None


def update_daily_password():
    business = Business.query.first()
    date = generate_time()
    if not business:
        return
    try:
        today = str(datetime.now().replace(microsecond=0).date())
        last_updated = business.updated
        if today > last_updated[0:10]:
            all_businesses = Business.query.all()
            for item in all_businesses:
                item.daily_password = generate_daily_password()
                item.updated = date
            database.session.commit()
    except Exception as e:
        print(e)
        database.session.rollback()
