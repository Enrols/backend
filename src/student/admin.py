from user.admin import UserAdmin
from django.contrib import admin
from .models import Student
from utils import format_phone_number
from django.utils.translation import gettext_lazy as _
# Register your models here.
class StudentAdmin(UserAdmin):
    list_display = ('email', 'full_name', 'phone_number', 'is_active')
    
    fieldsets = UserAdmin.fieldsets + (
        (_("Student Info"), {'fields': ('full_name', 'phone_number', 'email_verified', 'phone_number_verified')}),
        (_("Preferences"), {'fields': ('wishlist', 'interests', 'current_education_level', 'selected_tags', 'preferred_locations')})
    )
    
    filter_horizontal = ('wishlist', 'interests', 'preferred_locations', 'selected_tags')

    add_fieldsets = UserAdmin.add_fieldsets + (
        (_("Student Info"), {'fields': ('full_name', 'phone_number')}),
        (_("Preferences"), {'fields': ('wishlist', 'interests', 'current_education_level', 'selected_tags', 'preferred_locations')})
    )
    
    
    def save_model(self, request, obj, form, change):
        obj.phone_number = format_phone_number(obj.phone_number)
        return super().save_model(request, obj, form, change)

admin.site.register(Student, StudentAdmin)
