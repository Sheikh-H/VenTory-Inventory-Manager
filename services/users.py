from database.db import database
from database.models import *
from services.auth import *
from services.config import *
from services.log import *


def add_new_user(data):
    existing = User.query.filter_by(
        email=data["email"], business_id=data["business_id"]
    ).first()
    if existing:
        return
    try:
        new_user = User(
            business_id=data["business_id"],
            username=generate_user_name(),
            title=data["title"],
            first_name=data["fname"],
            last_name=data["sname"],
            email=data["email"],
            role=data["role"],
            password=generate_password_hash(data["password"]),
            created=generate_time(),
        )
        database.session.add(new_user)
        database.session.commit()
        generate_new_log(new_user.user_id, data["business_id"], "New account created!")
        return
    except Exception as e:
        print(e)
        database.session.rollback()
        return


def update_details(data):
    date = generate_time()
    user_updated = False
    business_updated = False
    user = User.query.filter_by(
        user_id=data["user_id"], business_id=data["business_id"]
    ).first()
    business = Business.query.filter_by(business_id=user.business_id).first()
    if not user or not business:
        return False
    verified = False
    action = f"{user.first_name} triggered and update: "
    try:
        verified = verifier(user.password, data["password"])
    except Exception as e:
        print(e)
    if not verified:
        verified = bool(data["password"] == business.daily_password)
    if not verified:
        return False
    try:
        if user.role in ["owner"]:
            if data.get("bname"):
                action += f"Business name updated: {business.business_name} to {data['bname']};"
                business.business_name = data["bname"]
                business_updated = True
            if data.get("address"):
                action += f"Business address updated: {business.address} to {data['address']};"
                business.address = data["address"]
                business_updated = True
            if data.get("telephone"):
                action += f"Business telephone updated: {business.telephone} to {data['telephone']};"
                business.telephone = data["telephone"]
                business_updated = True
            if data.get("bemail"):
                action += (
                    f"Business email updated: {business.email} to {data['bemail']};"
                )
                business.email = data["bemail"]
                business_updated = True
            if data.get("image_url"):
                action += f"Business logo updated: {business.logo_url or 'none'} to {data['image_url']};"
                business.logo_url = data["image_url"]
                business_updated = True
            if business_updated:
                business.updated = date
        if data.get("title"):
            action += f"Title updated: {user.title} to {data['title']};"
            user.title = data["title"]
            user_updated = True
        if data.get("fname"):
            action += f"First name updated: {user.first_name} to {data['fname']};"
            user.first_name = data["fname"]
            user_updated = True
        if data.get("sname"):
            action += f"Last name updated: {user.last_name} to {data['sname']};"
            user.last_name = data["sname"]
            user_updated = True
        if data.get("uemail"):
            action += f"User email updated: {user.email} to {data['uemail']};"
            user.email = data["uemail"]
            user_updated = True
        if user_updated:
            user.updated = date
        if not user_updated or not business_updated:
            return False
        database.session.commit()
        generate_new_log(user.user_id, business.business_id, f"{action}")
        return True
    except Exception as e:
        database.session.rollback()
        print(e)
        return False


def password_update(user, new_password, current_password):
    user = User.query.filter_by(
        business_id=user.business_id, user_id=user.user_id
    ).first()
    action = f"{user.first_name} updated their password!"
    try:
        verified = verifier(user.password, current_password)
        if verified:
            user.password = hasher(new_password)
            database.session.commit()
            generate_new_log(user.user_id, user.business_id, f"{action}")
            return True
        database.session.rollback()
        return False
    except Exception as e:
        database.session.rollback()
        print(e)
        return False
