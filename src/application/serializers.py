from rest_framework import serializers
from .models import Application, ApplicationFormResponseField, DocumentUpload
from course.serializers import CourseSerializer, BatchSerializer, ApplicationFormFieldsSerializer, RequiredDocumentsSerializer
from student.serializers import StudentSerializer
from course.models import Course, Batch, ApplicationFormField
from utils import format_phone_number
import mimetypes

class ApplicationFormSerializer(serializers.ModelSerializer):
    value_text = serializers.CharField(required=False, allow_null=True)
    value_number = serializers.FloatField(required=False, allow_null=True)
    form_details = ApplicationFormFieldsSerializer(many=False)
    
    class Meta:
        model = ApplicationFormResponseField
        
        fields = [
            'id',
            'form_details',
            'value_text',
            'value_number',
        ]
        
        
class ApplicationDocumentsSerializer(serializers.ModelSerializer):
    document_details = RequiredDocumentsSerializer(many=False)
    
    
    class Meta:
        model = DocumentUpload
        fields = [
            'id',
            'document_details',
            'file',
        ]

class ApplicationSerializer(serializers.ModelSerializer):
    course = CourseSerializer(many=False)
    batch_selected = BatchSerializer(many=False)

    class Meta:
        model = Application
        fields = [
            'id',
            'course',
            'batch_selected',
            'status',
            'submitted_on',
            'updated_on',
        ]
        
        
        
class ApplicationReqDocsSerializer(serializers.Serializer):
    file = serializers.FileField(
        max_length=100,
        allow_empty_file=False,
        use_url=False,
    )

    def validate_file(self, value):
        """
        Validate file type and size.
        """
        allowed_types = ["application/pdf", "image/jpeg", "image/png"]
        max_size = 5 * 1024 * 1024  # 5MB limit

        content_type, _ = mimetypes.guess_type(value.name)
        
        if content_type not in allowed_types:
            raise serializers.ValidationError("Only PDF, JPEG, and PNG files are allowed.")

        # if value.size > max_size:
        #     raise serializers.ValidationError("File size must be less than 5MB.")

        return value

class ApplicationDetailSerializer(serializers.ModelSerializer):
    form_data = ApplicationFormSerializer(many=True)
    course = CourseSerializer(many=False)
    batch_selected = BatchSerializer(many=False)
    applied_by = StudentSerializer(many=False)
    uploaded_docs = ApplicationDocumentsSerializer(many=True)
    
    class Meta:
        model = Application
        fields = [
            'id',
            'full_name',
            'phone_number',
            'email',
            'date_of_birth',
            
            'form_data',
            'uploaded_docs',
            'applied_by',
            'course',
            'batch_selected',
            
            'status',
            'submitted_on',
            'updated_on',
        ]
        
        read_only_fields = ['submitted_on', 'updated_on', 'status']

class ApplicationFormCreateSerializer(serializers.ModelSerializer):
    value_text = serializers.CharField(required=False, allow_null=True)
    value_number = serializers.FloatField(required=False, allow_null=True)
    form_details = serializers.PrimaryKeyRelatedField(queryset=ApplicationFormField.objects.all())  # Only ID for POST
    
    class Meta:
        model = ApplicationFormResponseField
        fields = [
            'form_details',
            'value_text',
            'value_number',
        ]

class ApplicationRequestSerializer(serializers.Serializer):
    full_name = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    date_of_birth = serializers.DateField(required=True)
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    batch_selected = serializers.PrimaryKeyRelatedField(queryset=Batch.objects.none())
    form_data = ApplicationFormCreateSerializer(many=True)
    

    def validate_phone_number(self, value):
        formatted_phone_number = format_phone_number(value)
        
        if formatted_phone_number is None:
            raise serializers.ValidationError("Enter a valid phone number")
        
        return formatted_phone_number

    def validate(self, data):
        course = data.get("course")
        batch_selected = data.get("batch_selected")

        if batch_selected and batch_selected.course != course:
            raise serializers.ValidationError({"batch_selected": "This batch does not belong to the selected course."})

        return data

    def __init__(self, *args, **kwargs):
        """
        Dynamically filter `batch_selected` choices based on the `course` field.
        """
        super().__init__(*args, **kwargs)
        if "course" in self.initial_data:
            try:
                course_id = self.initial_data.get('course')
                self.fields["batch_selected"].queryset = Batch.objects.filter(course_id=course_id)
            except ValueError:
                pass 
            
            
            
    def create(self, validated_data):
        form_data = validated_data.pop('form_data', [])
        applied_by = self.context['user']
        
        application = Application.objects.create(
            applied_by=applied_by, 
            full_name=validated_data.get('full_name'),
            phone_number=validated_data.get('phone_number'),
            email=validated_data.get('email'),
            date_of_birth=validated_data.get('date_of_birth'),
            course=validated_data.get('course'),
            batch_selected=validated_data.get('batch_selected'),
        )
        for entry in form_data:
            ApplicationFormResponseField.objects.create(application=application, **entry)
            
        return application
    
    
    def update(self, instance, validated_data):
        instance.full_name = validated_data.get('full_name', instance.full_name)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.email = validated_data.get('email', instance.email)
        instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
        
        instance.course = validated_data.get('course', instance.course)
        instance.batch_selected = validated_data.get('batch_selected', instance.batch_selected)

        form_data = validated_data.get('form_data')
        if form_data is not None:
            existing_fields = {field.form_details.id: field for field in instance.form_data.all()}
            
            for entry in form_data:
                field_id = entry["form_details"].id
                if field_id in existing_fields:

                    form_field = existing_fields[field_id]
                    form_field.value_text = entry.get("value_text", form_field.value_text)
                    form_field.value_number = entry.get("value_number", form_field.value_number)
                    form_field.save()
                else:
                    ApplicationFormResponseField.objects.create(application=instance, **entry)

        instance.save()
        return instance
    