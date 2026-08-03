import re

email_pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
price_pattern = r"^\d+(\.\d{1,2})?$"
date_pattern = r"^\d{4}-\d{2}-\d{2}$"
time_pattern = r"^\d{2}:\d{2}:\d{2} (AM|PM)$"
full_date_pattern = r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} (AM|PM)$"


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
    ]

    telephone = [
        "+",
        "(",
        ")",
        " ",
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

    if input_type == "text":
        for char in data:
            if char in forbidden_characters:
                return False

    if input_type == "email" and not re.fullmatch(email_pattern, data):
        return False

    if input_type == "number":
        for char in data:
            if char not in numbers:
                return False

    if input_type == "price" and not re.fullmatch(price_pattern, data):
        return False

    if input_type == "date" and (
        not re.fullmatch(full_date_pattern, data)
        and not re.fullmatch(time_pattern, data)
        and not re.fullmatch(date_pattern, data)
    ):
        return False

    if input_type == "telephone":
        for char in data:
            if char not in telephone:
                return False
    return True


def form_validation(data):
    if not data:
        return ""
    else:
        return data
