from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from preference.models import EducationLevel
from rest_framework.response import Response
from rest_framework import status
from django.db import IntegrityError
from preference.serializers import TagSerialzer, InterestSerializer, LocationSerializer
from course.serializers import CourseListSerializer
from user.authentication import IsStudent


class StudentEducationLevelView(APIView):
    """
    Handles the student's current education level.

    Methods:
        - POST: Sets or updates the student's current education level.
            
            Request Data:
                - education_level_id (int, required): ID of the education level.

            Responses:
                - 201 Created: Education level added successfully.
                - 400 Bad Request: Missing or invalid education_level_id.

        - DELETE: Removes the student's current education level.

            Responses:
                - 200 OK: Education level deleted successfully.
                
    """
    permission_classes = [IsStudent]

    def post(self,request):
        student = request.user

        education_level_id = request.data.get('education_level_id')
        if not education_level_id:
            return Response({'message': 'education_level_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        education_level = get_object_or_404(EducationLevel, id=education_level_id)
        student.current_education_level = education_level
        student.save()

        return Response({'message': 'Education level added successfully'}, status=status.HTTP_201_CREATED)
    
    def delete(self,request):
        student = request.user

        student.current_education_level = None
        student.save()

        return Response({'message': 'Education level deleted successfully'}, status=status.HTTP_200_OK)
    

class StudentTagListView(APIView):
    """
    Manages the tags selected by a student.

    Methods:
        get(request):
            Retrieves a list of tags selected by the student.

            Responses:
                - 200 OK: List of selected tags.

        post(request):
            Adds tags to the student's selected tags.

            Request Data:
                - tag_id (list of int, optional): List of tag IDs to add.

            Responses:
                - 201 Created: Tags added successfully.
                - 400 Bad Request: Invalid or non-existent tag ID.

        delete(request):
            Removes tags from the student's selected tags.

            Request Data:
                - tag_id (list of int, optional): List of tag IDs to remove.

            Responses:
                - 200 OK: Tags removed successfully.
    """
    permission_classes=[IsStudent]

    def get(self,request):
        student = request.user

        tags = student.selected_tags.all()
        tags_data = TagSerialzer(tags, many=True)

        return Response(tags_data.data, status=status.HTTP_200_OK)

    def post(self,request):

        student=request.user
        
        tag_ids = request.data.get('tag_id',[]) # There can be no tags also
        try:
            student.selected_tags.add(*tag_ids)
            student.save()
        except IntegrityError:
            return Response({'message': 'Tag does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'message': 'Tags added successfully'}, status=status.HTTP_201_CREATED)

    def delete(self,request):
        tag_ids = request.data.get('tag_id',[])
        student = request.user
        for tag_id in tag_ids:
            student.selected_tags.remove(tag_id)

        return Response({'message': 'Tags removed successfully'}, status=status.HTTP_200_OK)
    
class StudentInterestListView(APIView):
    """
    Manages the interests selected by a student.

    Methods:
        get(request):
            Retrieves a list of interests selected by the student.

            Responses:
                - 200 OK: List of selected interests.

        post(request):
            Adds interests to the student's selected interests.

            Request Data:
                - interest_id (list of int, optional): List of interest IDs to add.

            Responses:
                - 201 Created: Interests added successfully.
                - 400 Bad Request: Invalid or non-existent interest ID.

        delete(request):
            Removes interests from the student's selected interests.

            Request Data:
                - interest_id (list of int, optional): List of interest IDs to remove.

            Responses:
                - 200 OK: Interests removed successfully.
    """
    permission_classes=[IsStudent]

    def get(self,request):
        student=request.user
        interests = student.interests.all()
        interests_data = InterestSerializer(interests, many=True)

        return Response(interests_data.data, status=status.HTTP_200_OK)

    def post(self,request):
        student=request.user
        interest_ids = request.data.get('interest_id',[]) # There can be no interests also

        try:
            student.interests.add(*interest_ids)
            student.save()
        except IntegrityError:
            return Response({'message': 'Interest does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'message': 'Interests added successfully'}, status=status.HTTP_201_CREATED)
    
    def delete(self,request):
        interest_ids = request.data.get('interest_id',[])
        student = request.user
        for interest_id in interest_ids:
            student.interests.remove(interest_id)

        return Response({'message': 'Interests removed successfully'}, status=status.HTTP_200_OK)


class StudentLocationListView(APIView):
    """
    Manages the preferred locations of a student.

    Methods:
        get(request):
            Retrieves a list of the student's preferred locations.

            Responses:
                - 200 OK: List of preferred locations.

        post(request):
            Adds locations to the student's preferred locations.

            Request Data:
                - location_id (list of int, optional): List of location IDs to add.

            Responses:
                - 201 Created: Preferred locations added successfully.
                - 400 Bad Request: Invalid or non-existent location ID.

        delete(request):
            Removes locations from the student's preferred locations.

            Request Data:
                - location_id (list of int, optional): List of location IDs to remove.

            Responses:
                - 200 OK: Preferred locations removed successfully.
    """
    permission_classes=[IsStudent]

    def get(self,request):
        student = request.user
        locations = student.prefered_locations.all()
        serializer = LocationSerializer(locations,many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)

    def post(self,request):
        student = request.user

        location_ids = request.data.get('location_id',[]) # There can be no interests also

        try:
            student.prefered_locations.add(*location_ids)
            student.save()
        except IntegrityError:
            return Response({'message': 'Location does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Preferred locations added successfully'}, status=status.HTTP_201_CREATED)
    
    def delete(self,request):
        student = request.user

        location_ids = request.data.get('location_id',[])
        for location_id in location_ids:
            student.prefered_locations.remove(location_id)
        
        return Response({'message':'Preferred locations successfully removed'}, status=status.HTTP_200_OK)


class StudentWishListView(APIView):
    """
    Manages the student's wishlist for courses.

    Methods:
        get(request):
            Retrieves the courses in the student's wishlist.

            Responses:
                - 200 OK: List of courses in the wishlist.

        post(request):
            Adds a course to the student's wishlist.

            Request Data:
                - course_id (int, required): ID of the course to add.

            Responses:
                - 201 Created: Course added to wishlist successfully.
                - 400 Bad Request: Invalid or non-existent course ID.

        delete(request):
            Removes a course from the student's wishlist.

            Request Data:
                - course_id (int, required): ID of the course to remove.

            Responses:
                - 200 OK: Course removed from wishlist successfully.
    """
    permission_classes = [IsStudent]

    def get(self, request):
        student = request.user
        courses = student.wishlist.all()
        serializer = CourseListSerializer(courses, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        student = request.user

        course_id = request.data.get('course_id')

        if not course_id:
            return Response({'message': 'course_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            student.wishlist.add(course_id)
            student.save()
        except IntegrityError:
            return Response({'message': 'Course does not exist'}, status = status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Course added to wishlist successfully'}, status=status.HTTP_201_CREATED)
    
    def delete(self, request):
        student = request.user

        course_id = request.data.get('course_id')
        student.wishlist.remove(course_id)

        return Response({'message': 'Course deleted from wishlist'},status=status.HTTP_200_OK)
        