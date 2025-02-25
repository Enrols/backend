from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .serializers import ForgotPasswordSerializer, ResetPasswordSerializer, LoginOtpSerializer, LoginOtpVerifySerializer
from django.shortcuts import get_object_or_404
from .models import User, Otp
from .utils import create_token, decrypt_token
from datetime import datetime
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework import status
from emailclient.sender import send_password_reset_email, send_verification_email
from rest_framework_simplejwt.tokens import RefreshToken
import constants
from django.utils import timezone

datetime
class LoginOtpView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginOtpSerializer 
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        phone_number = serializer.validated_data('phone_number')
        user = get_object_or_404(User, phone_number=phone_number)
        
        otp = Otp(phone_number=phone_number)
        
        token = create_token({
            'phone_number': phone_number,
            'otp': otp.otp,
            'exp': otp.created_at + constants.OTP_EXP_TIME,
        })
        
        # todo write logic to send sms
        
        return Response({ 'token': token })
        

class LoginOtpVerifyView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginOtpVerifySerializer
    
    def post(self, request, token):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        otp = serializer.validated_data('otp')
        
        data = decrypt_token(token)
        if data['status'] is False:
            raise PermissionDenied("Token not valid")
        
        payload = data['payload']
        decoded_otp = payload['otp']
        phone_number = payload['phone_number']
        
        user = get_object_or_404(User, phone_number=phone_number)
        
        if (decoded_otp == otp):
            refresh_token = RefreshToken.for_user(user=user)
            access_token = refresh_token.access_token
            return Response({
                'access_token': str(access_token),
                'refresh_token': str(refresh_token),
            })
        else:
            raise PermissionDenied('OTP not valid')



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
            'exp': timezone.now() + constants.FORGOT_PASSWORD_EXP_TIME
        })
        
        
        try:
            send_password_reset_email(user.email, user.full_name, token)
        except:
            return Response({"error": "Mail server down"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({ 'message': 'mail sent successfully' })
        
        


class ResetPasswordView(APIView):
    permission_classes = [AllowAny]
    serializer_class = ResetPasswordSerializer
    
    def get(self, request, token):
        data = decrypt_token(token)
        
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
        datetime
        return Response({ 'message': 'reset password successful' })
        


class VerifyEmailView(APIView):
    def get(self, request):
        user = request.user
        
        token = create_token({
            'email': user.email,
            'exp': timezone.now() + constants.VERIFY_EMAIL_EXP_TIME
        })
        
        try:
            send_verification_email(user.email, user.full_name, token)
        except:
            return Response({"error": "Mail server down"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({ 'message': 'mail sent successfully' })


class VerifyEmailTokenView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, token):
        data = decrypt_token(token)
        
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
    