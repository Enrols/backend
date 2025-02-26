from django.db import models
from django.utils import timezone
import constants
from utils import generate_otp
from enum import Enum
class Otp(models.Model):
    """ OTP Model"""
    
    phone_number = models.CharField(max_length=20, unique=False)
    otp = models.CharField(max_length=6, unique=False, default=generate_otp)
    created_at = models.DateTimeField(default=timezone.now)
    def is_valid(self) -> bool:
        return (timezone.now()) > self.created_at + constants.OTP_EXP_TIME
        
    def get_expiration_time(self):
        return self.created_at + constants.OTP_EXP_TIME
    
    def __str__(self):
        return f"<< OTP: {self.phone_number}, {self.otp}, {'(expired)' if self.exp > timezone.now() else ''} >>"
    
    
class SmsType(Enum):
    TEST = 'TEST_FUNC'
    TWILIO = 'TWILIO'
    FAST2SMS = 'FAST2SMS'