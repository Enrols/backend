from rest_framework import serializers
from .models import Student

class LoginOtpSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=100)
    
    
class LoginOtpVerifySerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=6)
    
    
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['email', 'full_name', 'phone_number', 'email_verified', 'phone_number_verified', 'account_type']
