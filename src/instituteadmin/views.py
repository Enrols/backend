from django.shortcuts import render
from rest_framework.views import APIView
from course.serializers import CourseListSerializer
from .models import InstituteAdmin
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
# Create your views here.
class InstituteCourseListView(APIView):
    def get(self,request,id):
        institute = get_object_or_404(InstituteAdmin,id=id)
        obj = institute.offered_courses.all()
        serializer = CourseListSerializer(obj, many=True)
        return Response(serializer.data,status=200)