from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .serializers import LoginOtpSerializer, LoginOtpVerifySerializer
from django.shortcuts import get_object_or_404
from .models import Student
from smsclient.models import Otp
from utils import create_token, decrypt_token
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.tokens import RefreshToken
from smsclient.sender import send_otp_twilio
from utils import format_phone_number

class LoginOtpView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginOtpSerializer 
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        phone_number = serializer.validated_data['phone_number']
        phone_number = format_phone_number(phone_number=phone_number)
        user = get_object_or_404(Student, phone_number=phone_number)
        
        otp = Otp(phone_number=phone_number)
        
        token = create_token({
            'phone_number': phone_number,
            'otp': otp.otp,
            'exp': otp.get_expiration_time(),
        })
        
        # todo write logic to send sms
        send_otp_twilio(phone_number=phone_number, otp=otp.otp)
        
        return Response({ 'token': token })
        
    
class LoginOtpVerifyView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginOtpVerifySerializer
    
    def post(self, request, token):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        otp = serializer.validated_data['otp']
        
        data = decrypt_token(token)
        if data['status'] is False:
            raise PermissionDenied("Token not valid")
        
        payload = data['payload']
        decoded_otp = payload['otp']
        phone_number = payload['phone_number']
        
        user = get_object_or_404(Student, phone_number=phone_number)
        
        if (decoded_otp == otp):
            refresh_token = RefreshToken.for_user(user=user)
            access_token = refresh_token.access_token
            return Response({
                'access_token': str(access_token),
                'refresh_token': str(refresh_token),
            })
        else:
            raise PermissionDenied('OTP not valid')