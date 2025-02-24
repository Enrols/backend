from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .serializers import ForgotPasswordSerializer, ResetPasswordSerializer
from django.shortcuts import get_object_or_404
from .models import User
from .utils import create_token, decrypt_token
from datetime import datetime, timedelta
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, ValidationError

class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]
    serializer_class = ForgotPasswordSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        user = get_object_or_404(User, email=email)
        
        token = create_token({
            'email': user.email,
            'exp': datetime.now() + timedelta(minutes=30)
        })
        
        
        # Todo: logic to send email
        
        return Response({ 'message': 'mail sent successfully' })
        
        


class ResetPasswordView(APIView):
    permission_classes = [AllowAny]
    serializer_class = ResetPasswordSerializer
    
    def get(self, request, token):
        data = decrypt_token(token)
        print(data)
        
        if data['status'] is False:
            raise PermissionDenied("Token not valid")
        
        payload = data['payload']
        
        if 'email' not in payload:
            raise ValidationError("email not found in token")
        
        
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = payload['email']
        user = get_object_or_404(User, email)
        password = serializer.validated_data['password']
        
        user.set_password(password)
        
        return Response({ 'message': 'reset password successful' })
        


class VerifyEmailView(APIView):
    def get(self, request):
        user = request.user
        print(user)
        
        token = create_token({
            'email': user.email,
            'exp': datetime.now() + timedelta(hours=1)
        })
        
        print(token)
        # Todo: logic to send email
        
        return Response({ 'message': 'mail sent successfully' })


class VerifyEmailTokenView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, token):
        data = decrypt_token(token)
        print(data)
        
        if data['status'] is False:
            raise PermissionDenied("Token not valid")
        
        payload = data['payload']
        
        if 'email' not in payload:
            raise ValidationError("email not found in token")
        
        email = payload['email']
        user = get_object_or_404(User, email=email)
        
        user.email_verified = True 
        user.save()
        
        return Response({ 'message': 'email verified successfully' })
    