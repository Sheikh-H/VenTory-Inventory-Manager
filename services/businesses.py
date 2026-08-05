from flask import flash

from database.db import database
from database.models import *
from services.auth import *
from services.config import *
from services.log import *
from services.users import *


def new_business_registration(data):
    existing_business_name = Business.query.filter_by(
        business_name=data.get("name")
    ).first()
    existing_business_email = Business.query.filter_by(email=data.get("bemail")).first()
    existing_user_email = User.query.filter_by(email=data.get("uemail")).first()
    existing_business_user_email = Business.query.filter_by(
        email=data.get("uemail")
    ).first()
    existing_user_business_email = User.query.filter_by(
        email=data.get("bemail")
    ).first()
    request_time = generate_time()
    if (
        existing_business_name
        or existing_business_email
        or existing_user_email
        or existing_business_user_email
        or existing_user_business_email
    ):
        flash("Existing details, please try login or contact your admin!", "error")
        return False
    try:
        business_name = input_validator(
            data.get("name"), "text", minimum=3, maximum=255
        )
        business_address = input_validator(
            data.get("address"), "text", minimum=30, maximum=255
        )
        business_telephone = input_validator(data.get("telephone"), "telephone")
        business_email = input_validator(data.get("bemail"), "email")
        new_daily_password = generate_daily_password()
        new_business = Business(
            business_name=business_name,
            address=business_address,
            telephone=business_telephone,
            email=business_email,
            created=request_time,
            daily_password=new_daily_password,
        )
        database.session.add(new_business)
        database.session.commit()
        new_business_id = new_business.business_id
        new_username = generate_user_name()
        user_title = input_validator(data.get("title"), "title")
        user_fname = input_validator(data.get("fname"), "text", minimum=1, maximum=100)
        user_sname = input_validator(data.get("sname"), "text", minimum=1, maximum=100)
        user_email = input_validator(data.get("uemail"), "email")
        user_role = input_validator(data.get("role"), "role")
        user_password = input_validator(
            data.get("password"), "password", minimum=10, maximum=20
        )
        new_user = User(
            business_id=new_business_id,
            username=new_username,
            title=user_title,
            first_name=user_fname,
            last_name=user_sname,
            email=user_email,
            role=user_role,
            password=generate_password_hash(user_password),
            created=request_time,
        )
        database.session.add(new_user)
        database.session.commit()
        generate_new_log(
            new_user.user_id,
            new_business_id,
            f"{new_user.first_name} created an owner account and business called {new_business.business_name}",
        )
        flash("New account created successfully!", "success")
        return new_user.user_id
    except Exception as e:
        print(e)
        database.session.rollback()
        flash("Unable to create a new account, please try again!", "error")
        return None
