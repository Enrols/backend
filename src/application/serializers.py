from rest_framework import serializers
from .models import Application, ApplicationFormResponseField
from course.serializers import CourseSerializer, BatchSerializer, ApplicationFormFieldsSerializer
from student.serializers import StudentSerializer
from course.models import Course, Batch

class ApplicationFormSerializer(serializers.ModelSerializer):
    value_text = serializers.CharField(required=False, allow_blank=True)
    value_number = serializers.FloatField(required=False, allow_blank=True)
    value_field = serializers.FileField(required=False, allow_blank=True)
    form_details = ApplicationFormFieldsSerializer(many=False)
    
    class Meta:
        model = ApplicationFormResponseField
        
        fields = [
            'id',
            'form_details',
            'value_text',
            'value_number',
            'value_file',
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

class ApplicationDetailSerializer(serializers.ModelSerializer):
    form_data = ApplicationFormSerializer(many=True)
    course = CourseSerializer(many=False)
    batch_selected = BatchSerializer(many=False)
    applied_by = StudentSerializer(many=False)
    
    class Meta:
        model = Application
        fields = [
            'id',
            'full_name',
            'phone_number',
            'email',
            'date_of_birth',
            
            'form_data',
            'applied_by',
            'course',
            'batch_selected',
            
            'status',
            'submitted_on',
            'updated_on',
        ]
        
        read_only_fields = ['submitted_on', 'updated_on', 'status']

class ApplicationFormCreateSerializer(serializers.ModelSerializer):
    value_text = serializers.CharField(required=False, allow_blank=True)
    value_number = serializers.FloatField(required=False, allow_null=True)
    value_file = serializers.FileField(required=False, allow_null=True)
    form_details = serializers.PrimaryKeyRelatedField(queryset=ApplicationFormResponseField.objects.all())  # Only ID for POST

    class Meta:
        model = ApplicationFormResponseField
        fields = [
            'form_details',
            'value_text',
            'value_number',
            'value_file',
        ]

class ApplicationRequestSerializer(serializers.Serializer):
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    batch_selected = serializers.PrimaryKeyRelatedField(queryset=Batch.objects.none())
    form_data = ApplicationFormCreateSerializer(many=True)
    
    class Meta:
        model = Application
        fields = [
            'full_name',
            'phone_number',
            'email',
            'date_of_birth',
            'form_data',
            'course',
            'batch_selected',
        ]

    def validate(self, data):
        """
        Ensure that the selected batch belongs to the selected course.
        """
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
                course_id = self.initial_data["course"]
                self.fields["batch_selected"].queryset = Batch.objects.filter(course_id=course_id)
            except ValueError:
                pass  # If course_id is invalid, just leave queryset 