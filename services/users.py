from flask import flash

from database.db import database
from database.models import *
from services.auth import *
from services.config import *
from services.log import *
from services.validators import input_validator


def add_new_user(data):
    existing = User.query.filter_by(
        email=data["email"], business_id=data["business_id"]
    ).first()
    admin = User.query.filter_by(
        user_id=data.get("user_id"), business_id=data.get("business_id")
    ).first()
    if existing:
        return False
    try:
        title = input_validator(data.get("title"), "title")
        username = input_validator(data.get("username"), "text", minimum=10, maximum=10)
        fname = input_validator(data.get("fname"), "text", minimum=1, maximum=100)
        sname = input_validator(data.get("sname"), "text", minimum=1, maximum=100)
        email = input_validator(data.get("email"), "email")
        role = input_validator(data.get("role"), "role")
        if not all((title, username, fname, sname, email, role)):
            return False
        new_user = User(
            business_id=data["business_id"],
            username=username,
            title=title,
            first_name=fname,
            last_name=sname,
            email=email,
            role=role,
            password=generate_password_hash(data["password"]),
            created=generate_time(),
        )
        database.session.add(new_user)
        database.session.commit()
        generate_new_log(
            admin.user_id,
            admin.business_id,
            f"{admin.first_name} created a new account for {new_user.first_name}",
        )
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
    action = f"{user.first_name} updated their password!"
    valid_current = input_validator(current_password, "password")
    valid_new_password = input_validator(new_password, "password")
    verified = verifier(user.password, valid_current)
    if not verified:
        flash("Validation error, please try again!", "error")
        return False
    try:
        password = generate_password_hash(valid_new_password)
        user.password = password
        user.updated = date
        database.session.commit()
        generate_new_log(user.user_id, user.business_id, f"{action}")
        return True
    except Exception as e:
        database.session.rollback()
        print(e)
        return False


def update_details(data):
    date = generate_time()
    updates = False
    verified = False
    user_id = data.get("user_id")
    business_id = data.get("business_id")
    user = User.query.filter_by(user_id=user_id, business_id=business_id).first()
    business = Business.query.filter_by(business_id=business_id).first()
    action = (
        f"{user.first_name} triggered an update on their profile and they updated: "
    )
    if not user or not business:
        return False
    verified = bool(data["password"] == business.daily_password)
    if not verified:
        verified = verifier(user.password, data["password"])
        if not verified:
            flash("Unable to validate password!", "error")
            return False
    try:
        if user.role in ["owner"]:
            if data.get("bname"):
                action += f"Business name updated: {business.business_name} to {data['bname']};"
                business_name = input_validator(
                    data.get("bname"), "text", minimum=1, maximum=255
                )
                business.business_name = business_name
                updates = True
            if data.get("address"):
                action += f"Business address updated: {business.address} to {data['address']};"
                business_address = input_validator(data.get("address"), "address")
                business.address = business_address
                updates = True
            if data.get("telephone"):
                action += f"Business telephone updated: {business.telephone} to {data['telephone']};"
                business_telephone = input_validator(data.get("telephone"), "telephone")
                business.telephone = business_telephone
                updates = True
            if data.get("bemail"):
                action += (
                    f"Business email updated: {business.email} to {data['bemail']};"
                )
                business_email = input_validator(data.get("bemail"), "email")
                business.email = business_email
                updates = True
            if data.get("image_url"):
                action += f"Business logo updated: {business.logo_url or 'none'} to {data['image_url']};"
                business.logo_url = data.get("image_url")
                updates = True
            if updates:
                business.updated = date
                updates = False
        if data.get("title"):
            action += f"Title updated: {user.title} to {data['title']};"
            user_title = input_validator(data.get("title"), "title")
            user.title = user_title
            updates = True
        if data.get("fname"):
            action += f"First name updated: {user.first_name} to {data['fname']};"
            user_fname = input_validator(
                data.get("fname"), "text", minimum=1, maximum=100
            )
            user.first_name = user_fname
            updates = True
        if data.get("sname"):
            action += f"Last name updated: {user.last_name} to {data['sname']};"
            user_sname = input_validator(
                data.get("sname"), "text", minimum=1, maximum=100
            )
            user.last_name = user_sname
            updates = True
        if data.get("uemail"):
            action += f"User email updated: {user.email} to {data['uemail']};"
            user_email = input_validator(data.get("uemail"), "email")
            user.email = user_email
            updates = True
        if updates:
            user.updated = date
            updates = False
        database.session.commit()
        generate_new_log(user_id, business_id, action)
        return True
    except Exception as e:
        print(e)
        database.session.rollback()
        return False
