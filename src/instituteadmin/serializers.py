from rest_framework import serializers
from .models import InstituteAdmin, Detail

class DetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Detail
        fields = [
            'id',
            'detail',
            'info'
        ]

class InstituteAdminDetailSerializer(serializers.ModelSerializer):
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


class InstituteAdminSerializer(serializers.ModelSerializer):
    """id and name of InstituteAdmin"""
    class Meta:
        model = InstituteAdmin
        fields = [
            'id',
            'name'
        ]

