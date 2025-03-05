from rest_framework import serializers
from .models import InstituteAdmin, Detail

class DetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Detail
        fields = [
            'detail',
            'info'
        ]

class InstituteAdminSerializer(serializers.ModelSerializer):
    details = DetailSerializer(many=True)
    class Meta:
        model = InstituteAdmin
        fields = [
            'id',
            'email',
            'name', 
            'description', 
            'logo', ##
            'account_type',
            'details'
        ]


class InstituteAdminCompactSerializer(serializers.ModelSerializer):
    """id and name of InstituteAdmin"""
    class Meta:
        model = InstituteAdmin
        fields = [
            'id',
            'name'
        ]

