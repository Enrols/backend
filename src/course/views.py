from django.shortcuts import render
from .serializers import CourseListSerializer, CourseDetailSerializer
from .serializers import BatchSerializer
from rest_framework.views import APIView
from .models import Course
from preference.models import Location
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
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
        serializer = CourseListSerializer(courses, many=True)
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
        serializer = BatchSerializer(data=batches, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)