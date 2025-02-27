from user.admin import UserAdmin
from django.contrib import admin
from .models import Student, Interest, EducationLevel
from utils import format_phone_number
from django.utils.translation import gettext_lazy as _
# Register your models here.
class StudentAdmin(UserAdmin):
    list_display = ('email', 'full_name', 'phone_number', 'is_active')
    
    fieldsets = UserAdmin.fieldsets + (
        (_("Student Info"), {'fields': ('full_name', 'phone_number', 'email_verified', 'phone_number_verified')}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (_("Student Info"), {'fields': ('full_name', 'phone_number')}),
        (_("Preferences"), {'fields': ('wishlist', 'interests', 'current_education_level')})
    )
    
    
    def save_model(self, request, obj, form, change):
        obj.phone_number = format_phone_number(obj.phone_number)
        return super().save_model(request, obj, form, change)

class InterestAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

    def has_module_permission(self, request):
        return request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


class EducationLevelAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

    def has_module_permission(self, request):
        return request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser    

admin.site.register(Student, StudentAdmin)
admin.site.register(Interest, InterestAdmin)
admin.site.register(EducationLevel, EducationLevelAdmin)