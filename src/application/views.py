from django.shortcuts import render
from rest_framework.views import APIView
from user.authentication import IsStudent
from .serializers import ApplicationSerializer, ApplicationDetailSerializer
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Application
class ApplicationsListView(APIView):
    permission_classes = [IsStudent]
    request_serializer = None
    response_serializer = ApplicationSerializer
    
    
    def get(self, request):
        student = request.user
        applications = student.applications.all()
        serializer = self.response_serializer(applications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        pass


class ApplicationView(APIView):
    permission_classes = [IsStudent]
    request_serializer = None
    response_serializer = ApplicationDetailSerializer

    def get(self, request, id):
        student = request.user
        try:
            application = student.applications.get(id=id)
        except:
            return Response({'message': 'Application not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.response_serializer(application, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, id):
        pass

    def delete(self, request, id):
        pass

class ApplicationByCourseView(APIView):
    permission_classes = [IsStudent]

    def get(self, request, id):
        pass

    def put(self, request, id):
        pass

    def delete(self, request, id):
        pass 


class ApplicationByCourseSlugView(APIView):
    permission_classes = [IsStudent]

    def put(self, request, slug):
        pass

    def delete(self, request, slug):
        pass