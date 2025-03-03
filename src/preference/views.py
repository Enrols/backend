from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Tag, Exam, Skill, Stream, Interest, Location, EducationLevel
from .serializers import TagSerialzer, InterestSerializer, LocationSerializer, EducationLevelSerializer
from rest_framework.status import HTTP_200_OK
# Create your views here.
class TagListView(APIView):
    def get(self, _):
        obj = Tag.objects.all()
        serializer = TagSerialzer(obj, many=True)
        return Response(serializer.data,status=HTTP_200_OK)
    
class TagStreamListView(APIView):
    def get(self, _):
        obj = Stream.objects.all()
        serializer = TagSerialzer(obj, many=True)
        return Response(serializer.data,status=HTTP_200_OK)

class TagSkillListView(APIView):
    def get(self, _):
        obj = Skill.objects.all()
        serializer = TagSerialzer(obj, many=True)
        return Response(serializer.data,status=HTTP_200_OK)
    
class TagExamListView(APIView):
    def get(self, _):
        obj = Exam.objects.all()
        serializer = TagSerialzer(obj, many=True)
        return Response(serializer.data,status=HTTP_200_OK)
    
class InterestListView(APIView):
    def get(self, _):
        obj = Interest.objects.all()
        serializer = InterestSerializer(obj, many=True)
        return Response(serializer.data,status=HTTP_200_OK)
    
class LocationListView(APIView):
    def get(self, _):
        obj = Location.objects.all()
        serializer = LocationSerializer(obj, many=True)
        return Response(serializer.data,status=HTTP_200_OK)
    
class EducationLevelListView(APIView):
    def get(self, _):
        obj = EducationLevel.objects.all()
        serializer = EducationLevelSerializer(obj, many=True)
        return Response(serializer.data,status=HTTP_200_OK)
    