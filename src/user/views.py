from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import ForgotPasswordSerializer, ResetPasswordSerializer, LoginOtpSerializer, LoginOtpVerifySerializer, RegisterOtpSerializer, RegisterSerializer
from student.serializers import StudentSerializer
from instituteadmin.serializers import InstituteAdminDetailSerializer
from django.shortcuts import get_object_or_404
from student.models import Student
from .models import User
from utils import create_token, decrypt_token
from rest_framework.response import Response
from rest_framework import status
from emailclient.sender import send_password_reset_email, send_verification_email
import constants
from django.utils import timezone
from smsclient.models import Otp
from smsclient.sender import SmsClient
from rest_framework_simplejwt.tokens import RefreshToken

class ProfileView(APIView):
    """
    Retrieve the profile information for the authenticated user.

    Permissions:
        - Requires the user to be authenticated (IsAuthenticated).

    HTTP Methods:
        - GET: Returns the user's profile data based on their role.

    User Types:
        - If the user is a student, returns serialized data using `StudentSerializer`.
        - If the user is an institute admin, returns serialized data using `InstituteAdminDetailSerializer`.

    Responses:
        - 200 OK: Successfully returns the user's profile data.
        - 400 Bad Request: If the user type is invalid.

    Example Usage:
        GET /api/auth/profile/
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.is_student:
            serializer = StudentSerializer(user)
        elif user.is_institute:
            serializer = InstituteAdminDetailSerializer(user)
        else:
            return Response({"error": "Invalid user type"}, status=400)

        return Response(serializer.data)
    


class ForgotPasswordView(APIView):
    """
    Initiates the password reset process by sending an email with a reset link.

    Permissions:
        - Accessible to any user (AllowAny).

    HTTP Methods:
        - POST: Sends a password reset email if the provided email exists.

    Request Data:
        - email (str): The email address associated with the user's account.

    Responses:
        - 200 OK: Password reset email sent successfully.
        - 404 Not Found: If the provided email is not associated with any user.
        - 500 Internal Server Error: If the mail server is down.

    Example Usage:
        POST /api/auth/forgot-password/
    """

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
    """
    Resets the user's password using a valid token.

    Permissions:
        - Accessible to any user (AllowAny).

    HTTP Methods:
        - GET: Validates the reset token and updates the password.

    Request Data:
        - password (str): The new password to be set.

    Responses:
        - 200 OK: Password reset successfully.
        - 403 Forbidden: If the token is invalid or expired.
        - 400 Bad Request: If the email is missing from the token payload.

    Example Usage:
        GET /api/auth/reset-password/<token>/
    """
    permission_classes = [AllowAny]
    serializer_class = ResetPasswordSerializer
    
    def get(self, request, token):
        data = decrypt_token(token)
        
        if data['status'] is False:
            return Response({ 'message': "Token not valid" }, status=status.HTTP_403)
        
        payload = data['payload']
        
        if 'email' not in payload:
            return Response({ 'message': "email not found in token"}, status=status.HTTP_400_BAD_REQUEST)
        
        
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = payload['email']
        user = get_object_or_404(Student, email)
        password = serializer.validated_data['password']
        
        user.set_password(password)
        return Response({ 'message': 'reset password successful' })
        


class VerifyEmailView(APIView):
    """
    Sends an email verification link to the authenticated user.

    Permissions:
        - Requires the user to be authenticated (IsAuthenticated).

    HTTP Methods:
        - GET: Sends a verification email to the authenticated user.

    Responses:
        - 200 OK: Email sent successfully.
        - 500 Internal Server Error: If the mail server is down.

    Example Usage:
        GET /api/auth/send-verify-email/
    """
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        token = create_token({
            'email': user.email,
            'exp': timezone.now() + constants.VERIFY_EMAIL_EXP_TIME
        })
        
        try:
            send_verification_email(user.email, user.full_name, token)
        except:
            return Response({"message": "Mail server down"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({ 'message': 'mail sent successfully' })


class VerifyEmailTokenView(APIView):
    """
    Verifies the user's email address using a token.

    Permissions:
        - Accessible to any user (AllowAny).

    HTTP Methods:
        - GET: Verifies the email address using the provided token.

    Responses:
        - 200 OK: Email verified successfully.
        - 403 Forbidden: If the token is invalid or expired.
        - 400 Bad Request: If the email is missing from the token payload.

    Example Usage:
        GET /api/auth/verify-email/<token>/
    """
    permission_classes = [AllowAny]
    
    def get(self, _, token):
        data = decrypt_token(token)
        
        if data['status'] is False:
            return Response({ 'message': "Token not valid" }, status=status.HTTP_403_FORBIDDEN)
        
        payload = data['payload']
        
        if 'email' not in payload:
            return Response({ 'message': "Email not found in token" }, status=status.HTTP_400_BAD_REQUEST)
        
        email = payload['email']
        user = get_object_or_404(Student, email=email)
        
        user.email_verified = True 
        user.save()
        
        return Response({ 'message': 'email verified successfully' })
    


class LoginOtpView(APIView):
    """
    Initiates the OTP-based login process by sending an OTP to the user's phone number.

    Permissions:
        - Accessible to any user (AllowAny).

    HTTP Methods:
        - POST: Sends an OTP to the provided phone number.

    Request Data:
        - phone_number (str): The user's registered phone number.

    Responses:
        - 200 OK: OTP sent successfully along with a verification token.
        - 404 Not Found: If the phone number is not registered.

    Example Usage:
        POST /api/auth/student/login/otp/
    """
    permission_classes = [AllowAny]
    serializer_class = LoginOtpSerializer 
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        phone_number = serializer.validated_data['phone_number']
        get_object_or_404(Student, phone_number=phone_number)
        
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
    """
    Verifies the OTP and issues JWT access and refresh tokens.

    Permissions:
        - Accessible to any user (AllowAny).

    HTTP Methods:
        - POST: Verifies the OTP and returns access and refresh tokens.

    Request Data:
        - otp (str): The OTP received on the user's phone.

    Responses:
        - 200 OK: OTP verified successfully. Returns access and refresh tokens.
        - 403 Forbidden: If the OTP is invalid or expired.

    Example Usage:
        POST /api/auth/student/login/otp/<token>/
    """
    permission_classes = [AllowAny]
    serializer_class = LoginOtpVerifySerializer
    
    def post(self, request, token):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        otp = serializer.validated_data['otp']
        
        data = decrypt_token(token)
        if data['status'] is False:
            return Response({ 'message': "Token not valid" }, status=status.HTTP_403)
        
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
            return Response({ 'message': "OTP not valid"}, status=status.HTTP_403_FORBIDDEN)
        
        
        
        
class RegisterView(APIView):
    """
    Registers a new user account.

    Permissions:
        - Accessible to any user (AllowAny).

    HTTP Methods:
        - POST: Creates a new user account.

    Request Data:
        - email (str): The email for the new account
        - full_name (str): The name of the user
        - password (str): The password for the new account.
        - phone_number (str): User's phone number for OTP verification.

    Responses:
        - 201 Created: User created successfully.
        - 400 Bad Request: Validation errors.

    Example Usage:
        POST /api/auth/student/register/
    """
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        serializer.save()
        
        return Response({ 'message': 'User created successfully' }, status=status.HTTP_201_CREATED)
        


class RegisterOtpView(APIView):
    """
    Registers a new user and sends an OTP for phone number verification.

    Permissions:
        - Accessible to any user (AllowAny).

    HTTP Methods:
        - POST: Creates a new user and sends a verification OTP.

    Request Data:
        - phone_number (str): The user's phone number.
        - email (str): The user's email
        - full_name (str): The user's full name

    Responses:
        - 201 Created: User created successfully and OTP sent.
        - 400 Bad Request: Validation errors.

    Example Usage:
        POST /api/auth/student/register/otp/
    """
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
    """
    Verifies the user's phone number using an OTP.

    Permissions:
        - Accessible to any user (AllowAny).

    HTTP Methods:
        - POST: Verifies the OTP and marks the phone number as verified.

    Request Data:
        - otp (str): The OTP sent to the user's phone number.

    Responses:
        - 200 OK: Phone number verified successfully.
        - 403 Forbidden: If the OTP is invalid or expired.

    Example Usage:
        POST /api/auth/student/register/otp/<str:token>'
    """
    permission_classes = [AllowAny]
    serializer_class = LoginOtpVerifySerializer
    
    def post(self, request, token):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        otp = serializer.validated_data['otp']
        
        data = decrypt_token(token)
        if data['status'] is False:
            return Response({ 'message': "Token not valid" }, status=status.HTTP_403)
        
        payload = data['payload']
        decoded_otp = payload['otp']
        phone_number = payload['phone_number']
        
        user = get_object_or_404(Student, phone_number=phone_number)
        
        if (decoded_otp == otp):
            user.phone_number_verified = True
            user.save()
            return Response({'message': "Phone number verified successfully"})
        else:
            return Response({ 'message': "OTP not valid"}, status=status.HTTP_401_UNAUTHORIZED)
