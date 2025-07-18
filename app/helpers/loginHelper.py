import traceback
from argon2 import PasswordHasher
import re, time
import pyotp, pyqrcode


class security:
    def hash_password(self, password):
        return PasswordHasher().hash(password)

    def verify_password(self, hash_password, password):
        try:
            return PasswordHasher().verify(hash_password, password)
        except:
            return False

    def is_password_strong(self, password):
        errors = set()
        if len(password) < 8:
            errors.add("Need more than 8 characters.")
        if not re.search(r"[A-Z]", password):
            errors.add("At least one uppercase letter is required.")
        if not re.search(r"[a-z]", password):
            errors.add("At least one lowercase letter is required.")
        if not re.search(r"\d", password):
            errors.add("At least one digit is required.")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            errors.add("At least one special character is required.")


        # common_passwords = {
        #     "password",
        #     "123456",
        #     "123456789",
        #     "qwerty",
        #     "abc123",
        #     "password1",
        #     "12345678",
        #     "123",
        #     "1234",
        #     "0000",
        # }
        # if password.lower() in common_passwords:
        #     errors.add("The password is too common and easily guessable.")
        # else:
            # for item in common_passwords:
            #     if item in password.lower():
            #         errors.add("The password is too common and easily guessable.")

        if errors:
            return False, " ".join(errors)
        return True, "The password is strong."

    def TwoFA(self, email=None, otp=None, secret_key=None):
        try:
            if otp is None and email is not None:
                secret_key = pyotp.random_base32()
                url_qr = pyotp.totp.TOTP(secret_key).provisioning_uri(
                    email, issuer_name="CaptchaSonic"
                )
                url = pyqrcode.create(url_qr)
                print(f"URLS :: {url_qr, url}")
                b64 = url.png_as_base64_str(scale=8)
                print(f"B64 :: {b64}")
                secret_data = {"b64": b64, "secret_key": secret_key}
                return True, secret_data

            if otp is not None and secret_key is not None:
                totp = pyotp.TOTP(secret_key)
                if totp.now() == otp:
                    return True, totp.now()
                else:
                    return False, totp.now()
        except:
            traceback.print_exc()
            return False, None