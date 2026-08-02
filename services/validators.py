import re

email_pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
price_pattern = r"^\d+(\.\d{1,2})?$"
time_pattern = r"\d{2}:\dV{2}:\d{2} (AM|PM)$"
full_date_pattern = r"^\d{4}-\d{2}-\d{2} \d{2}:\dV{2}:\d{2} (AM|PM)$"
date_pattern = r"^\d{4}-\d{2}-\d{2}$"


def input_validator(data, input_type):
    forbidden_characters = ["<", ">", "{", "}", "[", "]"]

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
        "+",
        "(",
        ")",
        " ",
    ]

    if input_type == "text":
        for char in data:
            if char in forbidden_characters:
                return False, "Invalid input, try again!"

    if input_type == "email":
        if not re.fullmatch(email_pattern, data):
            return False, "Please enter a valid email address!"

    if input_type == "number":
        for char in data:
            if char not in numbers:
                return False, "Invalid numerical input, try again!"

    if input_type == "price":
        if not re.fullmatch(price_pattern, data):
            return False, "Please enter a valid price!"

    if input_type == "datetime":
        if (
            not re.fullmatch(full_date_pattern, data)
            or not re.fullmatch(time_pattern, data)
            or not re.fullmatch(date_pattern, data)
        ):
            return False, "Please enter a valid date/time!"
    return True, None
