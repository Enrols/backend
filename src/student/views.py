from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from preference.models import EducationLevel
from rest_framework.response import Response
from rest_framework import status
from django.db import IntegrityError
        
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
        