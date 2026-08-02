from database.db import database
from database.models import User
from services.auth import generate_password_hash, generate_time, generate_user_name
from services.log import generate_new_log


def add_new_user(data):
    existing = User.query.filter_by(email = data['email'], business_id=data['business_id']).first()
    if existing:
        return False, "Unable to register user!"
    try:
        new_user = User(
            business_id = data['business_id'],
            username = generate_user_name(),
            title = data['title'],
            first_name = data['fname'],
            last_name = data['sname'],
            email = data['email'],
            role = data['role'],
            password = generate_password_hash(data['password']),
            created = generate_time(),
            
        )
        database.session.add(new_user)
        database.session.commit()
        generate_new_log(new_user.id, data['business_id'], 'New account created!')
        return new_user.username
    except Exception as e:
        print(e)
        database.session.rollback()
        return None, "Unable to register user!"
