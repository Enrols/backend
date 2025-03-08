from .serializers import CourseSerializer, CourseDetailSerializer
from .serializers import BatchSerializer, ApplicationFormFieldsSerializer, RequiredDocumentsSerializer
from rest_framework.views import APIView
from .models import Course
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from user.authentication import IsStudent
# Create your views here.

class CourseListView(APIView):
    """
    Retrieve a list of all available courses.

    Permissions:
    - Only accessible to authenticated users (IsAuthenticated).

    HTTP Method:
    - GET: Returns a list of all `Course` objects.

    Response:
    - 200 OK: Returns a JSON list of courses.

    Example Usage:
    - GET /api/courses/
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
class CourseDetailView(APIView):
    """
    Retrieve details of a specific course.

    Permissions:
    - Only accessible to authenticated users (IsAuthenticated).

    HTTP Method:
    - GET: Returns details of a `Course` object based on the provided ID.

    Response:
    - 200 OK: Returns course details.
    - 404 Not Found: If the course with the given ID does not exist.

    Example Usage:
    - GET /api/courses/<id>/
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        course = get_object_or_404(Course, id=id)
        serializer = CourseDetailSerializer(course, many=False)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    
class CourseDetailSlugView(APIView):
    """
    Retrieve details of a specific course.

    Permissions:
    - Only accessible to authenticated users (IsAuthenticated).

    HTTP Method:
    - GET: Returns details of a `Course` object based on the provided slug.

    Response:
    - 200 OK: Returns course details.
    - 404 Not Found: If the course with the given ID does not exist.

    Example Usage:
    - GET /api/courses/<slug>/
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, slug):
        course = get_object_or_404(Course, slug=slug)
        serializer = CourseDetailSerializer(course)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    
class CourseBatchesListView(APIView):
    """
    Retrieve a list of locations where a specific course is available.

    Permissions:
    - Only accessible to authenticated users (IsAuthenticated).

    HTTP Method:
    - GET: Returns a list of locations associated with the specified course.

    Response:
    - 200 OK: Returns a JSON list of locations.
    - 404 Not Found: If the course with the given ID does not exist.

    Example Usage:
    - GET /api/courses/<id>/batches/
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        course = get_object_or_404(Course, id=id)
        batches = course.batches.all()
        serializer = BatchSerializer(batches, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class CourseBathcesListSlugView(APIView):
    """
    Retrieve a list of locations where a specific course is available.

    Permissions:
    - Only accessible to authenticated users (IsAuthenticated).

    HTTP Method:
    - GET: Returns a list of locations associated with the specified course.

    Response:
    - 200 OK: Returns a JSON list of locations.
    - 404 Not Found: If the course with the given ID does not exist.

    Example Usage:
    - GET /api/courses/<slug>/batches/
    """
    permission_classes = [IsAuthenticated] 
    
    def get(self, request, slug):
        course = get_object_or_404(Course, slug=slug)
        batches = course.batches.all()
        serializer = BatchSerializer(batches, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class CourseFormDetailsListView(APIView):
    """
    API endpoint to retrieve form details for a specific course using course ID.

    Path Parameters:
        - `id` (int): ID of the course.

    Returns:
        - **200 OK**: List of form fields required for the course.
        - **404 Not Found**: If the course does not exist.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, id):
        course = get_object_or_404(Course, id=id)
        form_fields = course.form_fields.all()
        serializer = ApplicationFormFieldsSerializer(form_fields, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
        
class CourseFormDetailsListSlugView(APIView):
    """
    API endpoint to retrieve form details for a specific course using course slug.

    Path Parameters:
        - `slug` (str): Slug of the course.

    Returns:
        - **200 OK**: List of form fields required for the course.
        - **404 Not Found**: If the course does not exist.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, slug):
        course = get_object_or_404(Course, slug=slug)
        form_fields = course.form_fields.all()
        serializer = ApplicationFormFieldsSerializer(form_fields, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class CourseReqDocsListView(APIView):
    """
    API endpoint to retrieve the list of required documents for a specific course using course ID.

    Path Parameters:
        - `id` (int): ID of the course.

    Returns:
        - **200 OK**: List of required documents for the course.
        - **404 Not Found**: If the course does not exist.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, id):
        course = get_object_or_404(Course, id=id)
        documents_required = course.documents_required.all()
        serializer = RequiredDocumentsSerializer(documents_required, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class CourseReqDocsListSlugView(APIView):
    """
    API endpoint to retrieve the list of required documents for a specific course using course slug.

    Path Parameters:
        - `slug` (str): Slug of the course.

    Returns:
        - **200 OK**: List of required documents for the course.
        - **404 Not Found**: If the course does not exist.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, slug):
        course = get_object_or_404(Course, slug=slug)
        documents_required = course.documents_required.all()
        serializer = RequiredDocumentsSerializer(documents_required, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)