from twilio.rest import Client
from django.conf import settings 
import constants
from .models import SmsType


class SmsClient:
    def __init__(self):
        try:
            self.type = SmsType(settings.SMS_TYPE)
        except:
            self.type = SmsType.TEST
        
        
        
    def send(self, phone_number: str, otp: str) -> str:
        if self.type == SmsType.TWILIO:
            return self.twilio(phone_number, otp)
        elif self.type == SmsType.FAST2SMS:
            return self.fast2sms(phone_number, otp)
        else:
            return self.test_sms(phone_number, otp)
    
    def test_sms(self, phone_number: str, otp: str) -> str:
        return "test-sms"
    
    def twilio(self, phone_number: str, otp: str) -> str:
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=f"Your OTP is {otp}. It is valid for {self.timedelta_to_string(constants.OTP_EXP_TIME)}.",
            from_=settings.TWILIO_PHONE_NUMBER,
            to=phone_number    
        )
        
        return message.sid
    
    
    def fast2sms(self, phone_number: str, otp: str) -> str:
        return "not-implemented"
    
    
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