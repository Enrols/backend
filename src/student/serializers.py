from rest_framework import serializers
from .models import Student
from utils import format_phone_number
from .models import Student
import secrets
import string

def generate_secure_string(length=16):
    characters = string.ascii_letters + string.digits  # A-Z, a-z, 0-9
    return ''.join(secrets.choice(characters) for _ in range(length))


class LoginOtpSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=100)
    
    def validate_phone_number(self, value):
        formatted_phone_number = format_phone_number(value)
        
        if formatted_phone_number is None:
            raise serializers.ValidationError("Enter a valid phone number")
        
        return formatted_phone_number
    
    
class LoginOtpVerifySerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=6)
    
    
class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=100)
    full_name = serializers.CharField(max_length=255)
    phone_number = serializers.CharField(max_length=20)
    password = serializers.CharField(max_length=100, write_only=True)
    
    def validate_phone_number(self, value):
        formatted_phone_number = format_phone_number(value)
        
        if formatted_phone_number is None:
            raise serializers.ValidationError("Enter a valid phone number")
        
        return formatted_phone_number
    
    
    def create(self, validated_data):
        email = validated_data['email']
        phone_number = validated_data['phone_number']
        full_name = validated_data['full_name']
        password = validated_data['password']
        
        student = Student(
            email=email,
            phone_number=phone_number,
            full_name=full_name,
        )
        
        student.set_password(password)
        student.save()
        return student
        
        
    
    
class RegisterOtpSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=100)
    full_name = serializers.CharField(max_length=255)
    phone_number = serializers.CharField(max_length=20)
    
    def validate_phone_number(self, value):
        formatted_phone_number = format_phone_number(value)
        
        if formatted_phone_number is None:
            raise serializers.ValidationError("Enter a valid phone number")
        
        return formatted_phone_number
    
    def create(self, validated_data) -> Student:
        email = validated_data['email']
        phone_number = validated_data['phone_number']
        full_name = validated_data['full_name']
        password = generate_secure_string()
        
        student = Student(
            email=email,
            phone_number=phone_number,
            full_name=full_name,
        )
        
        student.set_password(password)
        student.save()
        return student

        
        
    
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['email', 'full_name', 'phone_number', 'email_verified', 'phone_number_verified', 'account_type']
