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
from smsclient.sender import SmsClient
from .serializers import RegisterSerializer, RegisterOtpSerializer
from rest_framework import status

class LoginOtpView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginOtpSerializer 
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        phone_number = serializer.validated_data['phone_number']
        user = get_object_or_404(Student, phone_number=phone_number)
        
        otp = Otp(phone_number=phone_number)
        
        token = create_token({
            'phone_number': phone_number,
            'otp': otp.otp,
            'exp': otp.get_expiration_time(),
        })
        
        sms_client = SmsClient()
        sms_client.send(phone_number=phone_number, otp=otp.otp)
        
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
        
        
        
        
class RegisterView(APIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        serializer.save()
        
        return Response({ 'message': 'User created successfully' }, status=status.HTTP_201_CREATED)
        


class RegisterOtpView(APIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterOtpSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        student = serializer.save()
        phone_number = student.phone_number
        
        otp = Otp(phone_number=phone_number)
        
        token = create_token({
            'phone_number': phone_number,
            'otp': otp.otp,
            'exp': otp.get_expiration_time(),
        })
        
        sms_client = SmsClient()
        sms_client.send(phone_number=phone_number, otp=otp.otp)
        
        
        return Response({ 'message': 'User created successfully', 'token': token }, status=status.HTTP_201_CREATED)
    
    
class PhoneNumberVerifyView(APIView):
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
            user.phone_number_verified = True
            user.save()
            return Response({'message': "Phone number verified successfully"})
        else:
            raise PermissionDenied('OTP not valid')