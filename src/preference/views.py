from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Tag, Exam, Skill, Stream, Interest, Location, EducationLevel
from .serializers import TagSerialzer, InterestSerializer, LocationSerializer, EducationLevelSerializer

# Create your views here.
class TagListView(APIView):
    def get(self,request):
        obj = Tag.objects.all()
        serializer = TagSerialzer(obj, many=True)
        return Response(serializer.data,status=200)
    
class TagStreamListView(APIView):
    def get(self,request):
        obj = Stream.objects.all()
        serializer = TagSerialzer(obj, many=True)
        return Response(serializer.data,status=200)

class TagSkillListView(APIView):
    def get(self,request):
        obj = Skill.objects.all()
        serializer = TagSerialzer(obj, many=True)
        return Response(serializer.data,status=200)
    
class TagExamListView(APIView):
    def get(self,request):
        obj = Exam.objects.all()
        serializer = TagSerialzer(obj, many=True)
        return Response(serializer.data,status=200)
    
class InterestListView(APIView):
    def get(self,request):
        obj = Interest.objects.all()
        serializer = InterestSerializer(obj, many=True)
        return Response(serializer.data,status=200)
    
class LocationListView(APIView):
    def get(self,request):
        obj = Location.objects.all()
        serializer = LocationSerializer(obj, many=True)
        return Response(serializer.data,status=200)
    
class EducationLevelListView(APIView):
    def get(self,request):
        obj = EducationLevel.objects.all()
        serializer = EducationLevelSerializer(obj, many=True)
        return Response(serializer.data,status=200)
    