from rest_framework import serializers
from .models import Course, Batch, Duration, EligibilityCriterion
from instituteadmin.serializers import InstituteAdminCompactSerializer, InstituteAdminSerializer
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


class CourseListSerializer(serializers.ModelSerializer):    
    """For the card view of course"""
    offered_by = InstituteAdminCompactSerializer(many=False)
    tags = TagSerialzer(many=True)
    batches = BatchSerializer(BatchSerializer,many=True)
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
            'tags',
            'batches', 
            'duration'
        ]
    # def get_commencement_date(self, obj):
    #     first_batch = obj.batches.first()
    #     return first_batch.commencenment_date


class CourseDetailSerializer(serializers.ModelSerializer):
    offered_by = InstituteAdminSerializer(many=False)
    tags = TagSerialzer(many=True)
    batches = BatchSerializer(BatchSerializer,many=True)
    duration = DurationSerializer(many=False)
    eligibility_criteria = EligibilityCriterionSerializer(many=True)
    class Meta:
        model = Course
        fields = [
            'id',
            'name',
            'description',
            'mode',
            'image',##
            'offered_by',
            'batches',
            'tags',
            'duration',
            'eligibility_criteria',
            'fee_amount',
            'fee_breakdown',##
            'syllabus',##
            'slug'
        ]
    def get_image(self,obj):
        pass
    def get_fee_breakdown(self,obj):
        pass
    def get_syllabus(self,obj):
        pass