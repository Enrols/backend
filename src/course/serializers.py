from rest_framework import serializers
from .models import Course, Batch, Duration, EligibilityCriterion, ApplicationFormField, RequiredDocument
from instituteadmin.serializers import InstituteAdminSerializer, InstituteAdminDetailSerializer
from preference.serializers import TagSerialzer


class EligibilityCriterionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EligibilityCriterion
        fields = [
            'id',
            'detail'
        ]


class BatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batch
        fields = [
            'id',
            'location',
            'commencement_date',
            'discount'
        ]


class DurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Duration
        fields = [
            'hours',
            'days',
            'weeks',
            'months',
            'years'
        ]


class CourseSerializer(serializers.ModelSerializer):    
    """For the card view of course"""
    offered_by = InstituteAdminSerializer(many=False)
    # tags = TagSerialzer(many=True)
    # batches = BatchSerializer(many=True)
    # commencement_date = serializers.SerializerMethodField()
    duration = DurationSerializer(many=False)

    class Meta:
        model = Course
        fields = [
            'id',
            'name',
            'mode',
            'fee_amount',
            'image',
            'slug',
            'offered_by',
            # 'tags',
            # 'batches', 
            'duration'
        ]

class CourseDetailSerializer(serializers.ModelSerializer):
    offered_by = InstituteAdminDetailSerializer(many=False)
    tags = TagSerialzer(many=True)
    batches = BatchSerializer(many=True)
    duration = DurationSerializer(many=False)
    eligibility_criteria = EligibilityCriterionSerializer(many=True)
    class Meta:
        model = Course
        fields = [
            'id',
            'name',
            'description',
            'mode',
            'image',
            'offered_by',
            'batches',
            'tags',
            'duration',
            'eligibility_criteria',
            'fee_amount',
            'fee_breakdown',
            'syllabus',
            'slug'
        ]
        
        
class ApplicationFormFieldsSerializer(serializers.ModelSerializer):
    choices = serializers.SerializerMethodField()
    class Meta:
        model = ApplicationFormField
        fields = [
            'id',
            'field_name',
            'field_type',
            'choices',
            'helper_text',
            'required',
        ]
        
        
    def get_choices(self, obj: ApplicationFormField) -> list:
        return obj.choices.split(",") if obj.choices else []
    
    
class RequiredDocumentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequiredDocument
        fields = [
            'id',
            'file_name',
            'file_type',
        ]