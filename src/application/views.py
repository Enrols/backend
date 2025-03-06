from django.shortcuts import render
from rest_framework.views import APIView
from user.authentication import IsStudent
from .serializers import ApplicationSerializer, ApplicationDetailSerializer, ApplicationRequestSerializer, ApplicationReqDocsSerializer, ApplicationDocumentsSerializer 
from rest_framework.response import Response
from rest_framework import status
from .models import Application, DocumentUpload
from course.models import RequiredDocument
class ApplicationsListView(APIView):
    permission_classes = [IsStudent]
    request_serializer = ApplicationRequestSerializer
    response_serializer = ApplicationSerializer
    
    
    def get(self, request):
        student = request.user
        applications = student.applications.all()
        serializer = self.response_serializer(applications, many=True)        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        student = request.user
        serializer = self.request_serializer(data=request.data, context={ 'user': student })
        if serializer.is_valid():
            application = serializer.save()
            
            response_data = self.response_serializer(application).data
            
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApplicationView(APIView):
    permission_classes = [IsStudent]
    request_serializer = ApplicationRequestSerializer
    response_serializer = ApplicationDetailSerializer

    def get(self, request, id):
        student = request.user
        try:
            application = student.applications.get(id=id)
        except Application.DoesNotExist:
            return Response({'message': 'Application not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.response_serializer(application, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, id):
        student = request.user
        try:
            application = student.applications.get(id=id)
        except Application.DoesNotExist:
            return Response({'message': 'Application not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.request_serializer(application, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        student = request.user
        try:
            application = student.applications.get(id=id)
        except Application.DoesNotExist:
            return Response({ 'message': 'Application not found'}, status=status.HTTP_404_NOT_FOUND)
        
        application.delete()
        return Response({ 'message': "Application deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class ApplicationUploadDocView(APIView):
    permission_classes = [IsStudent]
    request_serializer = ApplicationReqDocsSerializer
    response_serializer = ApplicationDocumentsSerializer
    def post(self, request, id, doc_id):
        student = request.user
        serializer = self.request_serializer(data=request.FILES)
        serializer.is_valid(raise_exception=True)
        
        try:
            application = student.applications.get(id=id)
        except Application.DoesNotExist:
            return Response({ 'message': 'Application not found'}, status=status.HTTP_404_NOT_FOUND)
        
        
        try:
            required_doc_details = RequiredDocument.objects.get(id=doc_id)
            if required_doc_details.course != application.course:
                return Response({ 'message': 'Document details not found'}, status=status.HTTP_404_NOT_FOUND)
        except RequiredDocument.DoesNotExist:
            return Response({ 'message': 'Document details not found'}, status=status.HTTP_404_NOT_FOUND)
        
        
        document, _ = DocumentUpload.objects.update_or_create(
            document_details=required_doc_details,
            file=serializer.validated_data['file'],
            application=application
        )
        
        response_data = self.response_serializer(document).data 
        return Response(response_data, status=status.HTTP_200_OK)

class ApplicationByCourseView(APIView):
    permission_classes = [IsStudent]
    request_serializer = ApplicationRequestSerializer
    response_serizalizer = ApplicationDetailSerializer

    def get(self, request, id):
        student = request.user
        applications = student.applications.filter(course__id=id)

        if not applications.exists():
            return Response({'message': 'No applications found for this course'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.response_serizalizer(applications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        student = request.user
        try:
            application = student.applications.get(course__id=id)
        except Application.DoesNotExist:
            return Response({'message': 'Application not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.request_serializer(application, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        student = request.user
        try:
            application = student.applications.get(course__id=id)
        except Application.DoesNotExist:
            return Response({'message': 'Application not found'}, status=status.HTTP_404_NOT_FOUND)

        application.delete()
        return Response({'message': 'Application deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


class ApplicationByCourseSlugView(APIView):
    permission_classes = [IsStudent]
    request_serializer = ApplicationRequestSerializer
    response_serializer = ApplicationDetailSerializer

    def get(self, request, slug):
        student = request.user
        applications = student.applications.filter(course__slug=slug)

        if not applications.exists():
            return Response({'message': 'No applications found for this course'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.response_serializer(applications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, slug):
        student = request.user
        try:
            application = student.applications.get(course__slug=slug)
        except Application.DoesNotExist:
            return Response({'message': 'Application not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.request_serializer(application, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, slug):
        student = request.user
        try:
            application = student.applications.get(course__slug=slug)
        except Application.DoesNotExist:
            return Response({'message': 'Application not found'}, status=status.HTTP_404_NOT_FOUND)

        application.delete()
        return Response({'message': 'Application deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
