from django.shortcuts import render
from rest_framework.views import APIView
from course.serializers import CourseListSerializer
from .models import InstituteAdmin
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from user.authentication import IsStudent
# Create your views here.

class InstituteCourseListView(APIView):
    """
    Retrieve a list of courses offered by a specific institute.

    Permissions:
    - Only accessible to students (IsStudent).

    HTTP Method:
    - GET: Returns a list of all courses offered by the specified institute.

    Response:
    - 200 OK: Returns a JSON list of courses.
    - 404 Not Found: If the institute with the given ID does not exist.

    Example Usage:
    - GET /api/institutes/{id}/courses/
    """
    
    permission_classes = [IsStudent]
    
    def get(self, request, id):
        institute = get_object_or_404(InstituteAdmin,id=id)
        obj = institute.offered_courses.all()
        serializer = CourseListSerializer(obj, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)