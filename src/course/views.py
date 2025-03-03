from django.shortcuts import render
from .serializers import CourseListSerializer, CourseDetailSerializer
from preference.serializers import LocationSerializer
from rest_framework.views import APIView
from .models import Course
from preference.models import Location
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
# Create your views here.

class CourseListView(APIView):
    def get(self,request):
        courses = Course.objects.all()
        serializer = CourseListSerializer(courses, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
class CourseDetailView(APIView):
    def get(self,request,id):
        course = get_object_or_404(Course,id=id)
        serializer = CourseDetailSerializer(course, many=False)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
class CourseLocationListView(APIView):
    def get(self,request,id):
        course = get_object_or_404(Course,id=id)
        batches = course.batches.all()
        locations = Location.objects.filter(batches__in=batches)
        serializer = LocationSerializer(locations, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)