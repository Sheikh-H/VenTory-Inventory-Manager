from datetime import datetime

from database.db import database
from database.models import *
from services.auth import *
from services.config import *


def add_new_stock(data, user):
    date = str(datetime.now().replace(microsecond=0))
    for key, value in data.items():
        if not value:
            print(f"{key} is empty")
            generate_new_log(
                user.user_id,
                user.business_id,
                f"{user.first_name} attempted to add a product but had missing values",
            )
            return False
    action = ""
    try:
        new_stock = Stock(
            business_id=user.business_id,
            image_url=data["image_url"],
            title=data["title"],
            description=data["description"],
            price=data["price"],
            supplier=data["supplier"],
            created=date,
            available=data["quantity"],
        )
        database.session.add(new_stock)
        database.session.commit()
        action += f"{user.first_name} added new stock: {data['description']} - {data['quantity']} - £{data['price']} from {data['supplier']}"
        generate_new_log(user.user_id, user.business_id, f"{action}")
        return True
    except Exception as e:
        database.session.rollback()
        print(e)
        return False

