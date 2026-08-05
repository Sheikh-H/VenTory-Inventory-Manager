from datetime import datetime

from database.db import database
from database.models import *
from services.auth import *
from services.config import *


def add_new_stock(data, user):
    date = str(datetime.now().replace(microsecond=0))
    action = ""
    business = Business.query.filter_by(business_id=user.business_id).first()
    image = data.get("image")
    title = data.get("title")
    quantity = data.get("quantity")
    supplier = data.get("supplier")
    description = data.get("description")
    price = data.get("price")
    if not quantity or quantity == "" or quantity == None:
        quantity = 0
    if not price or price == "" or price == None:
        price = 0.00
    image_url = image_upload(image, f"stock-items/{title}", business.business_name)
    valid_title = input_validator(title, "text", minimum=1, maximum=50)
    valid_supplier = input_validator(supplier, "text", minimum=1, maximum=50)
    valid_description = input_validator(description, "text", maximum=255)
    try:
        new_stock = Stock(
            business_id=user.business_id,
            image_url=image_url,
            title=valid_title,
            description=valid_description,
            price=price,
            supplier=valid_supplier,
            created=date,
            available=quantity,
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
