from rest_framework import serializers


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=100)
    
    
class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=100)
    
    
class LoginOtpSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=100)
    
    
class LoginOtpVerifySerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=6)
    
    
from rest_framework import serializers
from user.models import Student, InstituteAdmin

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['email', 'full_name', 'phone_number', 'email_verified', 'phone_number_verified', 'account_type']

class InstituteAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstituteAdmin
        fields = ['email', 'name', 'description', 'logo', 'details', 'account_type']
