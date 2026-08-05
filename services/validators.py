import re

from services.config import *

email_pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
price_pattern = r"^\d+(\.\d{1,2})?$"
date_pattern = r"^\d{4}-\d{2}-\d{2}$"
time_pattern = r"^\d{2}:\d{2}:\d{2}$"
full_date_pattern = r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$"
numbers = [
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    0,
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "0",
]
telephone = [" ", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-"]
forbidden_characters = ["<", ">", "{", "}"]


def input_validator(data, input_type, minimum=None, maximum=None):
    if data is None:
        return None
    
    if maximum is not None and len(data) > maximum:
        return None
    
    if minimum is not None and len(data) < minimum:
        return None
    
    
    if input_type == "text":
        for char in data:
            if char in forbidden_characters:
                return None

    elif input_type == "email":
        
        for char in data:
            if char in forbidden_characters:
                return None
            
        if len(data) > 255 or len(data) < 6:
            return None
        
        if not re.fullmatch(email_pattern, data):
            return None

    elif input_type == "numerical":
        for char in data:
            if char not in numbers:
                return None
        if data < 0:
            return 0

    elif input_type == "price":
        if not re.fullmatch(price_pattern, data):
            return None
        if data < 0:
            return 0.00
        
    elif input_type == "date" and not (
        re.fullmatch(full_date_pattern, data)
        or re.fullmatch(time_pattern, data)
        or re.fullmatch(date_pattern, data)
    ):
        return None

    elif input_type == "telephone":
        for char in data:
            if char not in telephone:
                return None
        if len(data) > 13 or len(data) < 11:
            return None
        
    elif input_type == 'title':
        if len(data) > 3 or len(data) < 2:
            return None
        if data not in ['mr', 'mrs', 'miss', 'ms', 'dr']:
            return None

    return data

