from database.db import database
from database.models import Business, User
from services.auth import (
    generate_password_hash,
    generate_time,
    generate_user_name,
    update_daily_password,
)
from services.log import generate_new_log


def new_business_registration(data):
    try:
        existing_business = Business.query.filter_by(email=data["bemail"]).first()
        existing_user = User.query.filter_by(email=data["uemail"]).first()
        if existing_business and existing_business.business_name == data["name"]:
            return (
                None,
                "Existing business, please contact your administrator to login/register!",
            )
        if existing_user and existing_user.email == data["uemail"]:
            return (
                None,
                "Existing account, please login!",
            )
        new_business = Business(
            business_name=data["name"],
            address=data["address"],
            telephone=data["telephone"],
            email=data["bemail"],
            created=generate_time(),
            daily_password=update_daily_password(),
        )
        database.session.add(new_business)
        database.session.commit()
        _id = new_business.business_id
        new_user = User(
            business_id=_id,
            username=generate_user_name(),
            title=data["title"],
            first_name=data["fname"],
            last_name=data["sname"],
            email=data["uemail"],
            role=data["role"],
            password=generate_password_hash(data["password"]),
            created=new_business.created,
        )
        database.session.add(new_user)
        database.session.commit()
        generate_new_log(
            new_user.user_id,
            _id,
            f"New business and user created for {data['name']} by {data['fname']}!",
        )
        return new_user.user_id
    except Exception as e:
        database.session.rollback()
        print(e)
        return None
