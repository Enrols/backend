from rest_framework import serializers
from .models import Student

    
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['email', 'full_name', 'phone_number', 'email_verified', 'phone_number_verified', 'account_type']
