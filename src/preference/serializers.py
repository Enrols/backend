from rest_framework import serializers
from .models import Tag, Interest, Location, EducationLevel

class TagSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        fields = '__all__'

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

class EducationLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationLevel
        fields = '__all__'