from flask import flash

from database.db import database
from database.models import *
from services.auth import *
from services.config import *
from services.log import *
from services.validators import input_validator


def add_new_user(data):
    date = generate_time()

    admin = User.query.filter_by(
        user_id=data.get("admin_id"), business_id=data.get("business_id")
    ).first()

    if not admin:
        return False

    if admin.role != "owner":
        return False

    title = input_validator(data.get("title"), "title")
    username = input_validator(data.get("username"), "username")
    fname = input_validator(data.get("fname"), "text", minimum=1, maximum=100)
    sname = input_validator(data.get("sname"), "text", minimum=1, maximum=100)
    email = input_validator(data.get("email"), "email")
    role = input_validator(data.get("role"), "role")
    password = input_validator(data.get("password"), "password")
    if not all((title, username, fname, sname, email, role, password)):
        return False
    existing_user_email = User.query.filter_by(email=email).first()
    existing_business_email = Business.query.filter_by(email=email).first()
    existing_username = User.query.filter_by(username=username).first()

    if existing_user_email or existing_business_email or existing_username:
        return False

    try:

        if role not in ["employee", "manager"]:
            return False

        hashed_password = generate_password_hash(password)
        new_user = User(
            business_id=admin.business_id,
            username=username,
            title=title,
            first_name=fname,
            last_name=sname,
            email=email,
            role=role,
            password=hashed_password,
            created=date,
        )
        database.session.add(new_user)
        log_added = generate_new_log(
            admin.user_id,
            admin.business_id,
            f"{admin.first_name} created a new account for {new_user.first_name}",
        )
        if not log_added:
            database.session.rollback()
            return False
        database.session.commit()
        return True

    except Exception as e:
        print(e)
        database.session.rollback()
        return False


def password_update(user, new_password, current_password):
    date = generate_time()
    user = User.query.filter_by(
        business_id=user.business_id, user_id=user.user_id
    ).first()
    if not user:
        return False
    action = f"{user.first_name} updated their password!"
    valid_current = input_validator(current_password, "password")
    valid_new_password = input_validator(new_password, "password")
    if not valid_new_password:
        return False
    verified = None
    if user.password_reset == 0:
        if not valid_current:
            return False
        verified = verifier(user.password, valid_current)
    elif user.password_reset == 1:
        verified = True
    if not verified:
        flash("Validation error, please try again!", "error")
        return False
    try:
        password = generate_password_hash(valid_new_password)
        user.password = password
        user.updated = date
        user.password_reset = 0
        log_generated = generate_new_log(user.user_id, user.business_id, f"{action}")
        if not log_generated:
            database.session.rollback()
            return False
        database.session.commit()
        return True
    except Exception as e:
        database.session.rollback()
        print(e)
        return False


def update_details(data):
    date = generate_time()
    updates = False
    user_id = data.get("user_id")
    business_id = data.get("business_id")
    user = User.query.filter_by(user_id=user_id, business_id=business_id).first()
    business = Business.query.filter_by(business_id=business_id).first()

    if not user or not business:
        return False
    action = (
        f"{user.first_name} triggered an update on their profile and they updated: "
    )
    password = data.get("password")
    valid_password = input_validator(password, "password")
    if not valid_password:
        return False
    verified = bool(valid_password == business.daily_password)
    if not verified:
        verified = verifier(user.password, valid_password)
        if not verified:
            flash("Unable to validate password!", "error")
            return False
    try:
        if user.role == "owner":
            if data.get("bname"):
                business_name = input_validator(
                    data.get("bname"), "text", minimum=1, maximum=255
                )
                if not business_name:
                    return False
                else:
                    action += f"Business name updated: {business.business_name} to {business_name};"
                    business.business_name = business_name
                    updates = True
            if data.get("address"):
                business_address = input_validator(data.get("address"), "address")
                if not business_address:
                    return False
                else:
                    action += f"Business address updated: {business.address} to {business_address};"
                    business.address = business_address
                    updates = True
            if data.get("telephone"):
                business_telephone = input_validator(data.get("telephone"), "telephone")
                if not business_telephone:
                    return False
                else:
                    action += f"Business telephone updated: {business.telephone} to {business_telephone};"
                    business.telephone = business_telephone
                    updates = True
            if data.get("bemail"):
                business_email = input_validator(data.get("bemail"), "email")
                if not business_email:
                    return False
                else:
                    action += (
                        f"Business email updated: {business.email} to {business_email};"
                    )
                    business.email = business_email
                    updates = True
            if data.get("image"):
                image_url = image_upload(
                    data.get("image"), "logos", business.business_name
                )
                if not image_url:
                    return False
                else:
                    action += f"Business logo updated: {business.logo_url or 'none'} to {image_url};"
                    business.logo_url = image_url
                    updates = True
            if updates:
                business.updated = date
                updates = False
        if data.get("title"):
            user_title = input_validator(data.get("title"), "title")
            if not user_title:
                return False
            else:
                action += f"Title updated: {user.title} to {user_title};"
                user.title = user_title
                user.updated = date
                updates = True
        if data.get("fname"):
            user_fname = input_validator(
                data.get("fname"), "text", minimum=1, maximum=100
            )
            if not user_fname:
                return False
            else:
                action += f"First name updated: {user.first_name} to {user_fname};"
                user.first_name = user_fname
                user.updated = date
                updates = True
        if data.get("sname"):
            user_sname = input_validator(
                data.get("sname"), "text", minimum=1, maximum=100
            )
            if not user_sname:
                return False
            else:
                action += f"Last name updated: {user.last_name} to {user_sname};"
                user.last_name = user_sname
                user.updated = date
                updates = True
        if data.get("uemail"):
            user_email = input_validator(data.get("uemail"), "email")
            if not user_email:
                return False
            else:
                action += f"User email updated: {user.email} to {user_email};"
                user.email = user_email
                user.updated = date
                updates = True
        if not updates:
            return False
        log_created = generate_new_log(user_id, business_id, action)
        if not log_created:
            database.session.rollback()
            return False
        database.session.commit()
        return True
    except Exception as e:
        print(e)
        database.session.rollback()
        return False


def remove_user(data):
    if not data.get("user_id"):
        return False
    if not data.get("business_id"):
        return False
    if not data.get("delete_id"):
        return False
    admin = User.query.filter_by(
        user_id=data.get("user_id"), business_id=data.get("business_id")
    ).first()
    if not admin:
        return False
    if admin.role != "owner":
        return False
    action = f"{admin.first_name} deleted user: "
    try:
        delete_user = User.query.filter_by(
            user_id=data.get("delete_id"), business_id=admin.business_id
        ).first()
        if not delete_user:
            return False
        action += f"{delete_user.username} {delete_user.first_name} {delete_user.role}"
        if delete_user.role == "owner":
            return False
        if delete_user.username == admin.username:
            return False
        database.session.delete(delete_user)
        log_created = generate_new_log(admin.user_id, admin.business_id, action)
        if not log_created:
            database.session.rollback()
            return False
        database.session.commit()
        return True
    except Exception as e:
        print(e)
        database.session.rollback()
        return False


def forgot_password(data):
    if not data.get("username"):
        return False, None
    if not data.get("password"):
        return False, None
    valid_username = input_validator(data.get("username"), "username")
    valid_password = input_validator(data.get("password"), "password")
    if not valid_username or not valid_password:
        return False, None
    user = User.query.filter_by(username=valid_username).first()
    if not user:
        return False, None
    business = Business.query.filter_by(business_id=user.business_id).first()
    if not business:
        return False, None
    if valid_password == business.daily_password:
        try:
            user.password = generate_password_hash(generate_daily_password())
            user.password_reset = 1
            log_created = generate_new_log(
                user.user_id,
                user.business_id,
                f"{user.first_name} reset their own password with the daily password",
            )
            if not log_created:
                database.session.rollback()
                return False, None
            database.session.commit()
            return True, user.user_id
        except Exception as e:
            print(e)
            database.session.rollback()
            return False, None
    return False, None
