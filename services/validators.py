import re

email_pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"


def input_validator(data, form):
    forbidden_characters = ["<", ">", "{", "}", "[", "]"]

    ## Register Form
    if form == "register":
        new_user_fields = {
            "title",
            "fname",
            "sname",
            "email",
            "role",
            "password",
            "confirm",
        }

        new_business_fields = {"name", "address", "telephone", "email"}

        for section, fields in data.items():
            for key, value in fields.items():
                for character in value:
                    if character in forbidden_characters:
                        return False, "Invalid input, try again!"
                if value.strip() == "":
                    return False, "Please fill all fields!"

            if section == "business":
                received_fields = set(fields.keys())
                missing_fields = new_business_fields - received_fields

                if len(missing_fields) > 0:
                    return False, "Please use all fields!"

                for key, value in fields.items():
                    if key not in new_business_fields:
                        return False, "Please use form fields only!"

                if not re.fullmatch(email_pattern, fields.get("email")):
                    return False, "Please enter a valid email address!"

            if section == "user":
                received_fields = set(fields.keys())
                missing_fields = new_user_fields - received_fields

                if len(missing_fields) > 0:
                    return False, "Please use all fields!"

                for key, value in fields.items():
                    if key not in new_user_fields:
                        return False, "Please use form fields only!"

                    if key == "role":
                        if value not in ["owner", "employee", "manager"]:
                            return (
                                False,
                                "Please select a valid role, that best matches your position!",
                            )
                    if key == "title":
                        if value not in ["dr", "mr", "mrs", "miss", "ms"]:
                            return False, "Please use a valid title!"

                if not re.fullmatch(email_pattern, fields.get("email")):
                    return False, "Please enter a valid email address!"

                if fields.get("password") != fields.get("confirm"):
                    return False, "Please re-confirm your password!"

                if len(fields.get("confirm")) > 15 or len(fields.get("password")) > 15:
                    return False, "Password must be less than 15 characters!"

                if len(fields.get("confirm")) < 10 or len(fields.get("password")) < 10:
                    return False, "Password must be greater than 10 characters!"
    ## register form ^

    return True, None
