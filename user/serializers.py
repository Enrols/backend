from rest_framework import serializers


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=100)
    
    
class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=100)