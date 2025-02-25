from twilio.rest import Client
from django.conf import settings 
import constants

def timedelta_to_string(td):
    seconds = int(td.total_seconds())
    minutes = (seconds // 60) % 60
    hours = (seconds // 3600) % 24
    days = seconds // 86400

    parts = []
    if days:
        parts.append(f"{days} days")
    if hours:
        parts.append(f"{hours} hours")
    if minutes:
        parts.append(f"{minutes} minutes")

    return " ".join(parts) if parts else "0 minutes"

def send_otp_twilio(phone_number: str, otp: str) -> str:
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=f"Your OTP is {otp}. It is valid for {timedelta_to_string(constants.OTP_EXP_TIME)}.",
        from_=settings.TWILIO_PHONE_NUMBER,
        to=phone_number    
    )
    
    return message.sid