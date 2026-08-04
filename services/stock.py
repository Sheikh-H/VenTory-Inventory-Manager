from datetime import datetime

from database.models import *
from services.auth import *
from services.config import *


def add_new_stock(data):
    date = str(datetime.now().replace(microsecond=0))
    if not data['image_url']:
        return False
    action = ""
    try: 
        new_stock = Stock(
            business_id=data['business_id'],
            description=data['description'],
            price=data['price'],
            supplier=data['supplier'],
            
        )
        db.session.add(new_stock)
    return