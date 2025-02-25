from cryptography.fernet import Fernet
import jwt
from django.conf import settings
from random import randint
import constants

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