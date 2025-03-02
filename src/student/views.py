from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .serializers import LoginOtpSerializer, LoginOtpVerifySerializer
from django.shortcuts import get_object_or_404
from .models import Student
from preference.models import EducationLevel, Tag
from smsclient.models import Otp
from utils import create_token, decrypt_token
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.tokens import RefreshToken
from smsclient.sender import SmsClient
from .serializers import RegisterSerializer, RegisterOtpSerializer
from rest_framework import status
from django.db import IntegrityError

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
        
class StudentEducationLevelView(APIView):
    def post(self,request):
        student = request.user
        if(student.is_student==False):
            return Response({'message': 'Only students can add education level'}, status=status.HTTP_403_FORBIDDEN)
        education_level_id = request.data.get('education_level_id')
        if not education_level_id:
            return Response({'message': 'education_level_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        education_level = get_object_or_404(EducationLevel, id=education_level_id)
        student.current_education_level = education_level
        student.save()
        return Response({'message': 'Education level added successfully'}, status=status.HTTP_201_CREATED)
    
class StudentTagListView(APIView):
    def post(self,request):
        student=request.user
        if(student.is_student==False):
            return Response({'message': 'Only students can add tags'}, status=status.HTTP_403_FORBIDDEN)
        tags_id = request.data.get('tag_id',[]) # There can be no tags also
        try:
            student.selected_tags.add(*tags_id)
            student.save()
        except IntegrityError:
            return Response({'message': 'Tag does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Tags added successfully'}, status=status.HTTP_201_CREATED)

class StudentInterestListView(APIView):
    def post(self,request):
        student=request.user
        if(student.is_student==False):
            return Response({'message': 'Only students can add interests'}, status=status.HTTP_403_FORBIDDEN)
        interests_id = request.data.get('interest_id',[]) # There can be no interests also
        try:
            student.interests.add(*interests_id)
            student.save()
        except IntegrityError:
            return Response({'message': 'Interest does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Interests added successfully'}, status=status.HTTP_201_CREATED)

class StudentLocationListView(APIView):
    def post(self,request):
        student=request.user
        if(student.is_student==False):
            return Response({'message': 'Only students can add their preferred locations'}, status=status.HTTP_403_FORBIDDEN)
        locations_id = request.data.get('location_id',[]) # There can be no interests also
        try:
            student.prefered_locations.add(*locations_id)
            student.save()
        except IntegrityError:
            return Response({'message': 'Location does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Preferred locations added successfully'}, status=status.HTTP_201_CREATED)

class StudentWishListView(APIView):
    def post(self,request):
        student = request.user
        if(student.is_student==False):
            return Response({'message': 'Only students can add courses to their wishlist'}, status=status.HTTP_403_FORBIDDEN)
        course_id = request.data.get('course_id')
        if not course_id:
            return Response({'message': 'course_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            student.wishlist.add(course_id)
            student.save()
        except IntegrityError:
            return Response({'message': 'Course does not exist'}, status = status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Course added to wishlist successfully'}, status=status.HTTP_201_CREATED)
        