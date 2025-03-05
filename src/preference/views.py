from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Tag, Exam, Skill, Stream, Interest, Location, EducationLevel
from .serializers import TagSerialzer, InterestSerializer, LocationSerializer, EducationLevelSerializer
from rest_framework.status import HTTP_200_OK
# Create your views here.
class TagListView(APIView):
    """
    Retrieve a list of all available tags.

    Permissions:
    - Publicly accessible (AllowAny).

    HTTP Method:
    - GET: Returns a list of all `Tag` objects.

    Response:
    - 200 OK: Returns a JSON list of tags.

    Example Usage:
    - GET /api/tags/
    """
    
    permission_classes = [AllowAny]
    def get(self, _):
        obj = Tag.objects.all()
        serializer = TagSerialzer(obj, many=True)
        return Response(serializer.data,status=HTTP_200_OK)
    
class TagStreamListView(APIView):
    """
    Retrieve a list of all available streams.

    Permissions:
    - Publicly accessible (AllowAny).

    HTTP Method:
    - GET: Returns a list of all `Stream` objects.

    Response:
    - 200 OK: Returns a JSON list of streams.

    Example Usage:
    - GET /api/tags/streams/
    """
    
    permission_classes = [AllowAny]
    def get(self, _):
        obj = Stream.objects.all()
        serializer = TagSerialzer(obj, many=True)
        return Response(serializer.data,status=HTTP_200_OK)

class TagSkillListView(APIView):
    """
    Retrieve a list of all available skills.

    Permissions:
    - Publicly accessible (AllowAny).

    HTTP Method:
    - GET: Returns a list of all `Skill` objects.

    Response:
    - 200 OK: Returns a JSON list of skills.

    Example Usage:
    - GET /api/tags/skills/
    """
    
    permission_classes = [AllowAny]
    def get(self, _):
        obj = Skill.objects.all()
        serializer = TagSerialzer(obj, many=True)
        return Response(serializer.data,status=HTTP_200_OK)
    
class TagExamListView(APIView):
    """
    Retrieve a list of all available exams.

    Permissions:
    - Publicly accessible (AllowAny).

    HTTP Method:
    - GET: Returns a list of all `Exam` objects.

    Response:
    - 200 OK: Returns a JSON list of exams.

    Example Usage:
    - GET /api/tags/exams/
    """
    
    permission_classes = [AllowAny]
    def get(self, _):
        obj = Exam.objects.all()
        serializer = TagSerialzer(obj, many=True)
        return Response(serializer.data,status=HTTP_200_OK)
    
class InterestListView(APIView):
    """
    Retrieve a list of all available interests.

    Permissions:
    - Publicly accessible (AllowAny).

    HTTP Method:
    - GET: Returns a list of all `Interest` objects.

    Response:
    - 200 OK: Returns a JSON list of interests.

    Example Usage:
    - GET /api/interests/
    """
    
    permission_classes = [AllowAny]
    def get(self, _):
        obj = Interest.objects.all()
        serializer = InterestSerializer(obj, many=True)
        return Response(serializer.data,status=HTTP_200_OK)
    
class LocationListView(APIView):
    """
    Retrieve a list of all available locations.

    Permissions:
    - Publicly accessible (AllowAny).

    HTTP Method:
    - GET: Returns a list of all `Location` objects.

    Response:
    - 200 OK: Returns a JSON list of locations.

    Example Usage:
    - GET /api/locations/
    """
    
    permission_classes = [AllowAny]
    def get(self, _):
        obj = Location.objects.all()
        serializer = LocationSerializer(obj, many=True)
        return Response(serializer.data,status=HTTP_200_OK)
    
class EducationLevelListView(APIView):
    """
    Retrieve a list of all available education levels.

    Permissions:
    - Publicly accessible (AllowAny).

    HTTP Method:
    - GET: Returns a list of all `EducationLevel` objects.

    Response:
    - 200 OK: Returns a JSON list of education levels.

    Example Usage:
    - GET /api/education-levels/
    """
    
    permission_classes = [AllowAny]
    def get(self, _):
        obj = EducationLevel.objects.all()
        serializer = EducationLevelSerializer(obj, many=True)
        return Response(serializer.data,status=HTTP_200_OK)
    