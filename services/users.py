from database.db import database
from database.models import *
from services.auth import *
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


def update_details(data, method):
    date = generate_time()
    if method == "owner":
        try:
            user = User.query.filter_by(
                user_id=data["user_id"], business_id=data["business_id"]
            ).first()
            business = Business.query.filter_by(business_id=user.business_id).first()
            verified = login_user(user.username, data["password"])
            action = f"{user.first_name} triggered and update: "
            if verified:
                if data["title"]:
                    user.title = data["title"]
                    action += f"Title updated: {user.title} to {data['title']}"
                if data["fname"]:
                    user.first_name = data["fname"]
                    action += (
                        f"First name updated: {user.first_name} to {data['fname']}"
                    )
                if data["sname"]:
                    user.last_name = data["sname"]
                    action += f"Last name updated: {user.last_name} to {data['sname']}"
                if data["uemail"]:
                    user.email = data["uemail"]
                    action += f"User email updated: {user.email} to {data['uemail']}"
                user.updated = date
                database.session.commit()
                if data["name"]:
                    business.business_name = data["name"]
                    action += f"Business name updated: {business.business_name} to {data['name']}"
                if data["address"]:
                    business.address = data["address"]
                    action += f"Business address updated: {business.address} to {data['address']}"
                if data["telephone"]:
                    business.telephone = data["telephone"]
                    action += f"Business telephone updated: {business.telephone} to {data['telephone']}"
                if data["bemail"]:
                    business.email = data["bemail"]
                    action += f"Business email updated: {business.telephone} to {data['bemail']}"
                if data["image_url"]:
                    business.logo_url = data["image_url"]
                    action += f"Business logo updated: {business.logo_url or "none"} to {data['image_url']}"
                business.updated = date
                database.session.commit()
                generate_new_log(user.user_id, business.business_id, f"{action}")
                return True
            database.session.rollback()
            return False
        except Exception as e:
            database.session.rollback()
            print(e)
            return False
    if method == "user":
        try:
            user = User.query.filter_by(
                user_id=data["user_id"], business_id=data["business_id"]
            ).first()
            business = Business.query.filter_by(business_id=user.business_id).first()
            verified = bool(data["password"] == business.daily_password)
            action = f"{user.first_name} triggered and update: "
            if verified:
                if data["title"]:
                    user.title = data["title"]
                    action += f"User title updated: {user.title} to {data['title']}"
                if data["fname"]:
                    user.first_name = data["fname"]
                    action += (
                        f"User first name updated: {user.first_name} to {data['fname']}"
                    )
                if data["sname"]:
                    user.last_name = data["sname"]
                    action += (
                        f"User first name updated: {user.last_name} to {data['sname']}"
                    )
                if data["uemail"]:
                    user.email = data["uemail"]
                    action += (
                        f"User first name updated: {user.email} to {data['uemail']}"
                    )
                user.updated = date
                database.session.commit()
                generate_new_log(user.user_id, business.business_id, f"{action}")
                return True
            database.session.rollback()
            return False
        except Exception as e:
            database.session.rollback()
            print(e)
            return False


def password_update(user, new_password, current_password):
    user = User.query.filter_by(
        business_id=user.business_id, user_id=user.business_id
    ).first()
    action = f"{user.first_name} updated their password!"
    try:
        verified = verifier(user.password, current_password)
        if verified:
            if new_password:
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
