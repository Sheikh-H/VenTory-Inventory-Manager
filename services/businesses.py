from database.models import Business, User, Stock, Log
from services.auth import generate_time, update_daily_password
from database.db import database


def add_new_business(data):
    existing = Business.query.filter_by(email=data["email"]).first()
    if existing:
        if existing.business_name == data["name"]:
            if existing.telephone == data["telephone"]:
                if existing.email == data["email"]:
                    if existing.address == data["address"]:
                        return (
                            False,
                            "Existing business, please contact your administrator to login!",
                        )
    try:
        new_business = Business(
            business_name=data["name"],
            address=data["address"],
            telephone=data["telephone"],
            created=generate_time(),
            daily_password=update_daily_password(),
        )
        database.session.add(new_business)
        database.session.commit()
        return True, "New business added", new_business.id
    except Exception as e:
        database.session.rollback()
        print(e)
        return False, "Unable to add business!"
