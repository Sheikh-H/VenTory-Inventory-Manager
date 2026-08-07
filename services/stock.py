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
        action += f"{user.first_name} added new stock: {data['description']} {data['quantity']} £{data['price']} from {data['supplier']}"
        generate_new_log(user.user_id, user.business_id, f"{action}")
        return True
    except Exception as e:
        database.session.rollback()
        print(e)
        return False


def update_stock(data):
    date = str(datetime.now().replace(microsecond=0))
    user = User.query.filter_by(
        user_id=data.get("user_id"), business_id=data.get("business_id")
    ).first()
    if not user:
        return False
    business = Business.query.filter_by(business_id=user.business_id).first()
    if not business:
        return False
    stock = Stock.query.filter_by(
        business_id=user.business_id, stock_id=data.get("stock_id")
    ).first()
    if not stock:
        return False
    image = data.get("image")
    title = data.get("title")
    description = data.get("description")
    available = data.get("available")
    returned = data.get("returned")
    damaged = data.get("damaged")
    supplier = data.get("supplier")
    price = data.get("price")
    action = f"{user.first_name} updated stock {stock.stock_id} {stock.title};"
    valid_title = input_validator(title, "text", maximum=50)
    valid_description = input_validator(description, "text", maximum=255)
    valid_available = input_validator(available, "numerical")
    valid_returned = input_validator(returned, "numerical")
    valid_damaged = input_validator(damaged, "numerical")
    valid_supplier = input_validator(supplier, "text", maximum=50)
    valid_price = input_validator(price, "price")
    image_url = image_upload(
        image, f"stock-items/{valid_title or stock.title}", business.business_name
    )
    try:
        updates = False
        if valid_title:
            updates = True
            action += f"Stock title: {stock.title} to {valid_title};"
            stock.title = valid_title
        if valid_description:
            updates = True
            action += f"Stock description: {stock.description} to {valid_description};"
            stock.description = valid_description
        if valid_supplier:
            updates = True
            action += f"Supplier details: {stock.supplier} to {valid_supplier};"
            stock.supplier = valid_supplier
        if valid_available:
            updates = True
            action += f"Stock available: {stock.available} to {valid_available};"
            stock.available = valid_available
        if valid_returned:
            updates = True
            action += f"Stock returned: {stock.returned} to {valid_returned};"
            stock.returned = valid_returned
        if valid_damaged:
            updates = True
            action += f"Stock damaged: {stock.damaged} to {valid_damaged};"
            stock.damaged = valid_damaged
        if valid_price:
            updates = True
            action += f"Stock price: £{stock.price} to {valid_price};"
            stock.price = valid_price
        if image_url:
            updates = True
            action += f"Stock image updated and uploaded;"
            stock.image_url = image_url
        if updates:
            stock.updated = date
            generate_new_log(user.user_id, user.business_id, action)
            database.session.commit()
            return True
        return False
    except Exception as e:
        print(e)
        database.session.rollback()
        return False


def delete_item(data):
    if not data.get("stock_id"):
        return False
    if not data.get("business_id"):
        return False
    if not data.get("user_id"):
        return False
    user = User.query.filter_by(
        user_id=data.get("user_id"), business_id=data.get("user_id")
    ).first()
    if user.role not in ["owner", "manager"]:
        flash("Only manager and owner accounts are able to delete stock!", "error")
        return False
    if not user:
        return False
    action = f"{user.first_name} deleted stock: "
    try:
        stock = Stock.query.filter_by(
            business_id=data.get("business_id"), stock_id=data.get("stock_id")
        ).first()
        if stock is None:
            return False
        database.session.delete(stock)
        database.session.commit()
        action += f"{stock.title.title()} {stock.description.title()} availabe: {stock.available} returned:{stock.returned} damaged:{stock.damaged} price: {stock.price}"
        generate_new_log(data.get("user_id"), data.get("business_id"), action)
        return True
    except Exception as e:
        print(e)
        database.session.rollback()
        return False
