from cryptography.fernet import Fernet
import jwt
from django.conf import settings
from random import randint
import constants
import phonenumbers
from rest_framework.exceptions import ValidationError

JWT_SECRET = settings.SECRET_KEY
cipher_suite = Fernet(settings.FERNET_KEY)

def create_token(payload: dict) -> str:
    token = jwt.encode(payload, JWT_SECRET, algorithm='HS256')
    encrypted_token = cipher_suite.encrypt(token.encode()).decode()
    return encrypted_token


def decrypt_token(enc_token: str) -> dict:
    try:
        dec_token = cipher_suite.decrypt(enc_token.encode()).decode()
        payload = jwt.decode(dec_token, JWT_SECRET, algorithms=['HS256'])
        return {'payload': payload, 'status': True}
    except:
        return {'status': False}
    
    
def generate_otp(length: int = constants.OTP_LENGTH) -> str:
    otp = str(randint(0, (10 ** length) - 1)).zfill(length)
    return otp


def format_phone_number(phone_number: str, country_code: str = 'IN') -> str:
    try:
        parsed_number = phonenumbers.parse(phone_number, country_code)
        if phonenumbers.is_valid_number(parsed_number):
            return phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
        else:
            return None
    except phonenumbers.NumberParseException:
        return None
    
    

def validate_details(details):
    """ Ensure JSONField follows the structure: [{'detail': string, 'info': string}, ...] """
    if not isinstance(details, list):  # Ensure it's a list
        raise ValidationError("Details must be a list of objects.")

    for item in details:
        if not isinstance(item, dict):  # Each item must be a dictionary
            raise ValidationError("Each detail entry must be a dictionary.")
        if 'detail' not in item or 'info' not in item:
            raise ValidationError("Each dictionary must contain 'detail' and 'info' keys.")
        if not isinstance(item['detail'], str) or not isinstance(item['info'], str):
            raise ValidationError("'detail' and 'info' must be strings.")