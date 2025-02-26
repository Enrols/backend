from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from user.authentication import IsInstituteAdmin, IsStudent
# Create your views here.

class StudentOnlyTestView(APIView):
    permission_classes = [IsStudent]
    def get(self, request):
        return Response({ 'message': 'Hello World!'})

class InstituteOnlyTestView(APIView):
    permission_classes = [IsInstituteAdmin]
    def get(self, request):
        return Response({ 'message': 'Hello World!'})

class AnonTestView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        return Response({ 'message': 'Hello World!'})

class AuthedView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response({ 'message': 'Hello World!'})