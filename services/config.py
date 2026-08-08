import os
import secrets
from datetime import datetime

import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv
from flask import flash

load_dotenv()


def initialise_env():
    secret = secrets.token_hex(32)
    text = f"SECRET_KEY={secret}\n"
    if not os.path.exists(".env"):
        with open(".env", "w") as f:
            f.write(text)
    else:
        with open(".env", "r") as f:
            contents = f.read()
        if "SECRET_KEY=" not in contents:
            with open(".env", "a") as f:
                f.write(text)
        else:
            key = ""
            for line in contents.splitlines():
                if line.startswith("SECRET_KEY="):
                    key = line
                    break
            value = key.split("=", 1)[1].strip()
            if not value:
                updated_contents = ""
                for line in contents.splitlines():
                    if line.startswith("SECRET_KEY="):
                        updated_contents += f"SECRET_KEY={secret}\n"
                    else:
                        updated_contents += line + "\n"
                with open(".env", "w") as f:
                    f.write(updated_contents)


def generate_time():
    date = datetime.now().replace(microsecond=0).date()
    time = datetime.now().replace(microsecond=0).time()
    return f"{date} {time}"


def image_upload(image, folder, business_name):
    allowed_types = {"image/jpeg", "image/png", "image/webp"}

    if image.content_size != "5 * 1024 * 1024":
        flash("Images must be no larger than 5MB", "error")
        return None

    if image.content_type not in allowed_types:
        return None

    if not image or not image.filename:
        return None

    try:
        upload = cloudinary.uploader.upload(
            image,
            folder=f"VenTory-portfolio-project/{business_name}/{folder}",
        )
        return upload["secure_url"]

    except Exception as e:
        print(e)
        flash("Unable to upload image, try again!", "error")
        return None
