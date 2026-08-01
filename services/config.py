import os
import secrets

from dotenv import load_dotenv

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
