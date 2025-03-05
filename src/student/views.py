from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from preference.models import EducationLevel
from rest_framework.response import Response
from rest_framework import status
from preference.serializers import TagSerialzer, InterestSerializer, LocationSerializer, EducationLevelSerializer
from course.serializers import CourseListSerializer
from user.authentication import IsStudent
from .serializers import TagListRequestSerializer, EducationLevelRequestSerializer, InterestRequestSerializer, LocationRequestSerializer, WishListRequestSerializer
from preference.models import Interest, Tag, Location
from course.models import Course

class StudentEducationLevelView(APIView):
    """
    Manage the student's current education level.

    Permissions:
    - Only accessible to students (IsStudent).

    HTTP Methods:
    - POST: Set or update the student's current education level.
    - DELETE: Remove the student's current education level.

    Process:
    - POST:
        - Validates `education_level_id` from the request payload using `EducationLevelRequestSerializer`.
        - Fetches the corresponding `EducationLevel` object.
        - Assigns it to the student's `current_education_level` field.
        - Saves the student object.
        - Returns a success response.
    - DELETE:
        - Resets the `current_education_level` field to `None`.
        - Saves the student object.
        - Returns a success response.

    Responses:
    - 201 Created: Education level successfully updated.
    - 200 OK: Education level successfully removed.
    - 404 Not Found: If the provided `education_level_id` does not exist.

    Example Usage:
    - GET /api/students/education-level/
    
    - POST /api/students/education-level/
    Payload:
    ```json
    {
        "education_level_id": 2
    }
    ```

    - DELETE /api/students/education-level/
    """
    
    permission_classes = [IsStudent]
    request_serializer = EducationLevelRequestSerializer
    response_serializer = EducationLevelSerializer
    
    def get(self, request):
        student = request.user
        
        education_level = student.current_education_level
        education_level_data = self.response_serializer(education_level)

        return Response(education_level_data.data, status=status.HTTP_200_OK)        
        

    def post(self,request):
        student = request.user
        serializer = self.request_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        education_level_id = serializer.validated_data['education_level_id']
        
        
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
    Manage the student's selected tags.

    Permissions:
    - Only accessible to students (IsStudent).

    HTTP Methods:
    - GET: Retrieve the list of selected tags.
    - POST: Add tags to the student's profile.
    - DELETE: Remove specific tags from the student's profile.

    Process:
    - GET:
        - Retrieves all tags currently selected by the student.
        - Returns serialized tag data.
    - POST:
        - Validates `tag_ids` from the request payload using `TagListRequestSerializer`.
        - Checks if all provided `tag_ids` exist in the database.
        - Adds only valid tags to the student's `selected_tags`.
        - If any `tag_ids` are invalid, returns an error with the missing IDs.
    - DELETE:
        - Validates `tag_ids` from the request payload.
        - Removes the specified tags from the student's `selected_tags`.

    Responses:
    - 200 OK: Successfully retrieved or removed tags.
    - 201 Created: Tags successfully added.
    - 400 Bad Request: If `tag_ids` are invalid or missing.

    Example Usage:
    - GET /api/students/tags/

    - POST /api/students/tags/
    Payload:
    ```json
    {
        "tag_ids": [1, 2, 3]
    }
    ```

    - DELETE /api/students/tags/
    Payload:
    ```json
    {
        "tag_ids": [1, 2]
    }
    ```
    """
    
    permission_classes=[IsStudent]
    request_serializer = TagListRequestSerializer
    response_serializer = TagSerialzer
    
    def get(self,request):
        student = request.user

        tags = student.selected_tags.all()
        tags_data = self.response_serializer(tags, many=True)

        return Response(tags_data.data, status=status.HTTP_200_OK)

    def post(self,request):
        student = request.user
        serializer = self.request_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tag_ids = serializer.validated_data['tag_ids']
        
        existing_tags = set(Tag.objects.filter(id__in=tag_ids).values_list('id', flat=True))
        missing_tags = set(tag_ids) - existing_tags
        
        if missing_tags:
            return Response({'message': f"Invalid tag IDs: {missing_tags}"}, status=status.HTTP_400_BAD_REQUEST)
    
        student.selected_tags.add(*existing_tags)
        return Response({'message': 'Tags added successfully'}, status=status.HTTP_201_CREATED)

    def delete(self,request):
        serializer = self.request_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tag_ids = serializer.validated_data['tag_ids']
        
        student = request.user
        for tag_id in tag_ids:
            student.selected_tags.remove(tag_id)

        return Response({'message': 'Tags removed successfully'}, status=status.HTTP_200_OK)
    
class StudentInterestListView(APIView):
    """
    Manage the student's selected interests.

    Permissions:
    - Only accessible to students (IsStudent).

    HTTP Methods:
    - GET: Retrieve the list of selected interests.
    - POST: Add interests to the student's profile.
    - DELETE: Remove specific interests from the student's profile.

    Process:
    - GET:
        - Retrieves all interests currently selected by the student.
        - Returns serialized interest data.
    - POST:
        - Validates `interest_ids` from the request payload using `InterestRequestSerializer`.
        - Checks if all provided `interest_ids` exist in the database.
        - Adds only valid interests to the student's `interests`.
        - If any `interest_ids` are invalid, returns an error with the missing IDs.
    - DELETE:
        - Validates `interest_ids` from the request payload.
        - Removes the specified interests from the student's `interests`.

    Responses:
    - 200 OK: Successfully retrieved or removed interests.
    - 201 Created: Interests successfully added.
    - 400 Bad Request: If `interest_ids` are invalid or missing.

    Example Usage:
    - GET /api/students/interests/

    - POST /api/students/interests/
    Payload:
    ```json
    {
        "interest_ids": [1, 2, 3]
    }
    ```

    - DELETE /api/students/interests/
    Payload:
    ```json
    {
        "interest_ids": [1, 2]
    }
    ```
    """
    
    permission_classes=[IsStudent]
    request_seriazlier = InterestRequestSerializer
    response_serializer = InterestSerializer

    def get(self,request):
        student = request.user
        interests = student.interests.all()
        interests_data = self.response_serializer(interests, many=True)

        return Response(interests_data.data, status=status.HTTP_200_OK)

    def post(self,request):
        student = request.user
        serializer = self.request_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        interest_ids = serializer.validated_data['interest_ids']

        existing_interests = set(Interest.objects.filter(id__in=interest_ids).values_list('id', flat=True))
        missing_interests = set(interest_ids) - existing_interests
        
        if missing_interests:
            return Response({'message': f'Invalid interest IDs: {list(missing_interests)}'}, status=status.HTTP_400_BAD_REQUEST)

        student.interests.add(*existing_interests)
        
        return Response({'message': 'Interests added successfully'}, status=status.HTTP_201_CREATED)
    
    def delete(self,request):
        student = request.user
        serializer = self.request_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        interest_ids = serializer.validated_data['interest_ids']
        
        for interest_id in interest_ids:
            student.interests.remove(interest_id)

        return Response({'message': 'Interests removed successfully'}, status=status.HTTP_200_OK)


class StudentLocationListView(APIView):
    """
    Manage the student's preferred locations.

    Permissions:
    - Only accessible to students (IsStudent).

    HTTP Methods:
    - GET: Retrieve the list of preferred locations.
    - POST: Add locations to the student's preferences.
    - DELETE: Remove specific locations from the student's preferences.

    Process:
    - GET:
        - Retrieves all locations currently selected by the student.
        - Returns serialized location data.
    - POST:
        - Validates `location_ids` from the request payload using `LocationRequestSerializer`.
        - Checks if all provided `location_ids` exist in the database.
        - Adds only valid locations to the student's `preferred_locations`.
        - If any `location_ids` are invalid, returns an error with the missing IDs.
    - DELETE:
        - Validates `location_ids` from the request payload.
        - Removes the specified locations from the student's `preferred_locations`.

    Responses:
    - 200 OK: Successfully retrieved or removed locations.
    - 201 Created: Locations successfully added.
    - 400 Bad Request: If `location_ids` are invalid or missing.

    Example Usage:
    - GET /api/students/preferred-locations/

    - POST /api/students/preferred-locations/
    Payload:
    ```json
    {
        "location_ids": [1, 2, 3]
    }
    ```

    - DELETE /api/students/preferred-locations/
    Payload:
    ```json
    {
        "location_ids": [1, 2]
    }
    ```
    """
    
    permission_classes=[IsStudent]
    request_serializer = LocationRequestSerializer
    response_serializer = LocationSerializer

    def get(self,request):
        student = request.user
        locations = student.preferred_locations.all()
        serializer = self.response_serializer(locations,many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)

    def post(self,request):
        student = request.user
        serailizer = self.request_serializer(data=request.data)
        serailizer.is_valid(raise_exception=True)
        location_ids = serailizer.validated_data['location_ids']
        
        existing_locations = set(Location.objects.filter(id__in=location_ids).values_list('id', flat=True))
        missing_locations = set(location_ids) - existing_locations
        
        if missing_locations:
            return Response({'message': f"Invalid Location IDs: {missing_locations}"}, status=status.HTTP_400_BAD_REQUEST)
        
        student.preferred_locations.add(*existing_locations)
        return Response({'message': 'Preferred locations added successfully'}, status=status.HTTP_201_CREATED)
    
    def delete(self,request):
        student = request.user
        serailizer = self.request_serializer(data=request.data)
        serailizer.is_valid(raise_exception=True)
        location_ids = serailizer.validated_data['location_ids']
        
        for location_id in location_ids:
            student.preferred_locations.remove(location_id)
        
        return Response({'message':'Preferred locations successfully removed'}, status=status.HTTP_200_OK)


class StudentWishListView(APIView):
    """
    Manage the student's wishlist of courses.

    Permissions:
    - Only accessible to students (IsStudent).

    HTTP Methods:
    - GET: Retrieve the list of courses in the student's wishlist.
    - POST: Add a course to the student's wishlist.
    - DELETE: Remove a course from the student's wishlist.

    Process:
    - GET:
        - Retrieves all courses currently in the student's wishlist.
        - Returns serialized course data.
    - POST:
        - Validates `course_id` from the request payload using `WishListRequestSerializer`.
        - Checks if the course exists in the database.
        - If valid, adds the course to the student's wishlist.
        - If the course does not exist, returns an error.
    - DELETE:
        - Validates `course_id` from the request payload.
        - Removes the specified course from the student's wishlist.

    Responses:
    - 200 OK: Successfully retrieved or removed course from wishlist.
    - 201 Created: Course successfully added to wishlist.
    - 400 Bad Request: If `course_id` is invalid or the course does not exist.

    Example Usage:
    - GET /api/students/wishlist/

    - POST /api/students/wishlist/
    Payload:
    ```json
    {
        "course_id": 1
    }
    ```

    - DELETE /api/students/wishlist/
    Payload:
    ```json
    {
        "course_id": 1
    }
    ```
    """
    
    permission_classes = [IsStudent]
    request_serializer = WishListRequestSerializer
    response_serializer = CourseListSerializer

    def get(self, request):
        student = request.user
        courses = student.wishlist.all()
        serializer = self.response_serializer(courses, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        student = request.user
        serializer = self.request_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        course_id = serializer.validated_data['course_id']

        if not Course.objects.filter(id=course_id).exists():
            return Response({'message': 'Course does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        student.wishlist.add(course_id)

        return Response({'message': 'Course added to wishlist successfully'}, status=status.HTTP_201_CREATED)
    
    def delete(self, request):
        student = request.user
        serializer = WishListRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        course_id = serializer.validated_data['course_id']
        student.wishlist.remove(course_id)

        return Response({'message': 'Course deleted from wishlist'},status=status.HTTP_200_OK)
        