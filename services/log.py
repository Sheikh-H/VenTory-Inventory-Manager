from database.db import database
from database.models import *
from services.auth import *


def generate_new_log(user_id, business_id, action):
    try:
        new_log = Log(
            user_id=user_id,
            business_id=business_id,
            timestamp=generate_time(),
            comment=action,
        )
        database.session.add(new_log)
        database.session.commit()
        return True
    except Exception as e:
        database.session.rollback()
        print(e)
        return False
