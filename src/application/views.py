from django.shortcuts import render
from rest_framework.views import APIView
from user.authentication import IsStudent
from .serializers import ApplicationSerializer, ApplicationDetailSerializer, ApplicationRequestSerializer, ApplicationReqDocsSerializer, ApplicationDocumentsSerializer 
from rest_framework.response import Response
from rest_framework import status
from .models import Application, DocumentUpload
from course.models import RequiredDocument
class ApplicationsListView(APIView):
    """
    API endpoint to list and create student applications.

    - **GET**: Retrieve all applications submitted by the authenticated student.
    - **POST**: Submit a new application.

    Serializers:
        - `request_serializer`: ApplicationRequestSerializer (For creating applications)
        - `response_serializer`: ApplicationSerializer (For listing applications)
    """
    
    permission_classes = [IsStudent]
    request_serializer = ApplicationRequestSerializer
    response_serializer = ApplicationSerializer
    
    def get(self, request):
        """
        Retrieve all applications submitted by the authenticated student.

        Returns:
            - **200 OK**: List of serialized applications.
        """
        student = request.user
        applications = student.applications.all()
        serializer = self.response_serializer(applications, many=True)        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        """
        Submit a new application.

        Request Body (ApplicationRequestSerializer):
            - full_name (str): Student's full name.
            - phone_number (str): Contact number.
            - email (str): Email address.
            - date_of_birth (date): Date of birth.
            - course (int): Course ID.
            - batch_selected (int): Batch ID.
            - form_data (list): List of form responses.

        Returns:
            - **201 Created**: Successfully created application.
            - **400 Bad Request**: Validation errors.
        """
        student = request.user
        serializer = self.request_serializer(data=request.data, context={ 'user': student })
        if serializer.is_valid():
            application = serializer.save()
            
            response_data = self.response_serializer(application).data
            
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApplicationView(APIView):
    """
    API endpoint to retrieve, update, and delete a specific application.

    - **GET**: Retrieve details of a specific application.
    - **PUT**: Update an existing application.
    - **DELETE**: Remove an application.

    Serializers:
        - `request_serializer`: ApplicationRequestSerializer (For updating applications)
        - `response_serializer`: ApplicationDetailSerializer (For retrieving application details)
    """
    permission_classes = [IsStudent]
    request_serializer = ApplicationRequestSerializer
    response_serializer = ApplicationDetailSerializer

    def get(self, request, id):
        """
        Retrieve the details of a specific application.

        Path Parameter:
            - `id` (int): ID of the application to retrieve.

        Returns:
            - **200 OK**: Application details.
            - **404 Not Found**: If the application does not exist.
        """
        student = request.user
        try:
            application = student.applications.get(id=id)
        except Application.DoesNotExist:
            return Response({'message': 'Application not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.response_serializer(application, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, id):
        """
        Update an existing application.

        Path Parameter:
            - `id` (int): ID of the application to update.

        Request Body (ApplicationRequestSerializer):
            - full_name (str): Student's full name.
            - phone_number (str): Contact number.
            - email (str): Email address.
            - date_of_birth (date): Date of birth.
            - course (int): Course ID.
            - batch_selected (int): Batch ID.
            - form_data (list): List of form responses.

        Returns:
            - **200 OK**: Updated application details.
            - **400 Bad Request**: Validation errors.
            - **404 Not Found**: If the application does not exist.
        """
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
        """
        Delete an application.

        Path Parameter:
            - `id` (int): ID of the application to delete.

        Returns:
            - **204 No Content**: Successfully deleted the application.
            - **404 Not Found**: If the application does not exist.
        """
        student = request.user
        try:
            application = student.applications.get(id=id)
        except Application.DoesNotExist:
            return Response({ 'message': 'Application not found'}, status=status.HTTP_404_NOT_FOUND)
        
        application.delete()
        return Response({ 'message': "Application deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class ApplicationUploadDocView(APIView):
    """
    API endpoint for uploading required documents for an application.

    - **POST**: Upload a document for a specific application.

    Serializers:
        - `request_serializer`: ApplicationReqDocsSerializer (For validating uploaded files)
        - `response_serializer`: ApplicationDocumentsSerializer (For returning the uploaded document details)
    """
    permission_classes = [IsStudent]
    request_serializer = ApplicationReqDocsSerializer
    response_serializer = ApplicationDocumentsSerializer
    
    
    def post(self, request, id, doc_id):
        """
        Upload a required document for a student's application.

        Path Parameters:
            - `id` (int): ID of the application.
            - `doc_id` (int): ID of the required document type.

        Request Body (ApplicationReqDocsSerializer):
            - file (File): The document file to be uploaded.

        Returns:
            - **200 OK**: Document successfully uploaded/updated.
            - **400 Bad Request**: Validation errors.
            - **404 Not Found**: If the application or required document is not found.
        """
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
    """
    API endpoint for managing applications based on course ID.

    - **GET**: Retrieve all applications for a specific course.
    - **PUT**: Update an application for a specific course.
    - **DELETE**: Delete an application for a specific course.

    Serializers:
        - `request_serializer`: ApplicationRequestSerializer (For application update requests)
        - `response_serializer`: ApplicationDetailSerializer (For returning application details)
    """
    permission_classes = [IsStudent]
    request_serializer = ApplicationRequestSerializer
    response_serizalizer = ApplicationDetailSerializer

    def get(self, request, id):
        """
        Retrieve all applications for a specific course.

        Path Parameters:
            - `id` (int): ID of the course.

        Returns:
            - **200 OK**: List of applications for the course.
            - **404 Not Found**: If no applications exist for the given course.
        """
        student = request.user
        applications = student.applications.filter(course__id=id)

        if not applications.exists():
            return Response({'message': 'No applications found for this course'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.response_serizalizer(applications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        """
        Update an application for a specific course.

        Path Parameters:
            - `id` (int): ID of the course.

        Request Body (ApplicationRequestSerializer):
            - Any updatable fields of the application.

        Returns:
            - **200 OK**: Updated application details.
            - **400 Bad Request**: Validation errors.
            - **404 Not Found**: If the application for the course does not exist.
        """
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
        """
        Delete an application for a specific course.

        Path Parameters:
            - `id` (int): ID of the course.

        Returns:
            - **204 No Content**: Application deleted successfully.
            - **404 Not Found**: If the application for the course does not exist.
        """
        student = request.user
        try:
            application = student.applications.get(course__id=id)
        except Application.DoesNotExist:
            return Response({'message': 'Application not found'}, status=status.HTTP_404_NOT_FOUND)

        application.delete()
        return Response({'message': 'Application deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


class ApplicationByCourseSlugView(APIView):
    """
    API endpoint for managing applications based on a course slug.

    - **GET**: Retrieve all applications for a specific course using the course slug.
    - **PUT**: Update an application for a specific course using the course slug.
    - **DELETE**: Delete an application for a specific course using the course slug.

    Serializers:
        - `request_serializer`: ApplicationRequestSerializer (For application update requests)
        - `response_serializer`: ApplicationDetailSerializer (For returning application details)
    """
    permission_classes = [IsStudent]
    request_serializer = ApplicationRequestSerializer
    response_serializer = ApplicationDetailSerializer

    def get(self, request, slug):
        """
        Retrieve all applications for a specific course using the course slug.

        Path Parameters:
            - `slug` (str): Slug of the course.

        Returns:
            - **200 OK**: List of applications for the course.
            - **404 Not Found**: If no applications exist for the given course slug.
        """
        student = request.user
        applications = student.applications.filter(course__slug=slug)

        if not applications.exists():
            return Response({'message': 'No applications found for this course'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.response_serializer(applications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, slug):
        """
        Update an application for a specific course using the course slug.

        Path Parameters:
            - `slug` (str): Slug of the course.

        Request Body (ApplicationRequestSerializer):
            - Any updatable fields of the application.

        Returns:
            - **200 OK**: Updated application details.
            - **400 Bad Request**: Validation errors.
            - **404 Not Found**: If the application for the course does not exist.
        """
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
        """
        Delete an application for a specific course using the course slug.

        Path Parameters:
            - `slug` (str): Slug of the course.

        Returns:
            - **204 No Content**: Application deleted successfully.
            - **404 Not Found**: If the application for the course does not exist.
        """
        student = request.user
        try:
            application = student.applications.get(course__slug=slug)
        except Application.DoesNotExist:
            return Response({'message': 'Application not found'}, status=status.HTTP_404_NOT_FOUND)

        application.delete()
        return Response({'message': 'Application deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
