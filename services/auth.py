from argon2 import PasswordHasher
from datetime import datetime, timedelta

hasher = PasswordHasher().hash
verifier = PasswordHasher().verify


def create_new_user(user):
    date_time = datetime.now().replace(microsecond=0)
    username = user["username"]
    password = hasher(user["password"])
    
