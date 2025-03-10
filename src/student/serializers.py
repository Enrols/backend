from rest_framework import serializers
from .models import Student

    
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = [
            'id',
            'email',
            'full_name',
            'phone_number',
            'email_verified',
            'phone_number_verified',
            'account_type',
        ]


class EducationLevelRequestSerializer(serializers.Serializer):
    education_level_id = serializers.IntegerField(min_value=1)


class TagListRequestSerializer(serializers.Serializer):
    tag_ids = serializers.ListField(
        child=serializers.IntegerField(min_value=1),
        allow_empty=True,
    )
    
class InterestRequestSerializer(serializers.Serializer):
    interest_ids = serializers.ListField(
        child=serializers.IntegerField(min_value=1),
        allow_empty=True,
    )
    
    
class LocationRequestSerializer(serializers.Serializer):
    location_ids = serializers.ListField(
        child=serializers.IntegerField(min_value=1),
        allow_empty=True,
    )
    
class WishListRequestSerializer(serializers.Serializer):
    course_id = serializers.IntegerField(min_value=1)