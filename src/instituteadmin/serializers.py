from rest_framework import serializers
from .models import InstituteAdmin

class InstituteAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstituteAdmin
        fields = ['email', 'name', 'description', 'logo', 'details', 'account_type']
