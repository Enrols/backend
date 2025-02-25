from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, Student, InstituteAdmin, Otp
from .utils import format_phone_number

# Base User Admin Configuration
class UserAdmin(BaseUserAdmin):
    """ Custom User Admin Panel """
    
    list_display = ('email', 'account_type', 'is_active', 'is_staff', 'date_joined')
    list_filter = ('account_type', 'is_active', 'is_staff')
    ordering = ('-date_joined',)
    search_fields = ('email',)

    fieldsets = (
        (_("User Information"), {"fields": ("email", "password")}),
        (_("User Type"), {"fields": ("account_type",)}),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser")}),
        (_("Important Dates"), {"fields": ("date_joined",)}),
    )

    add_fieldsets = (
        (_("Create User"), {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2"),
        }),
    )

    readonly_fields = ('date_joined',)  # Prevent editing 'date_joined'


# 🔹 Student Admin
class StudentAdmin(UserAdmin):
    list_display = ('email', 'full_name', 'phone_number', 'is_active')
    
    fieldsets = UserAdmin.fieldsets + (
        (_("Student Info"), {'fields': ('full_name', 'phone_number', 'email_verified', 'phone_number_verified')}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (_("Student Info"), {'fields': ('full_name', 'phone_number')}),
    )
    
    
    def save_model(self, request, obj, form, change):
        obj.phone_number = format_phone_number(obj.phone_number)
        return super().save_model(request, obj, form, change)

# 🔹 Institute Admin
class InstituteAdminAdmin(UserAdmin):
    list_display = ('email', 'name', 'is_active', 'is_staff')

    fieldsets = UserAdmin.fieldsets + (
        (_("Institute Info"), {'fields': ('name', 'description', 'logo', 'details')}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (_("Institute Info"), {'fields': ('name', 'description', 'logo', 'details')}),
    )

# OTP Admin Configuration
class OtpAdmin(admin.ModelAdmin):
    """ Admin panel for OTPs """
    
    list_display = ('phone_number', 'otp', 'created_at', 'is_valid')
    search_fields = ('phone_number', 'otp')

    readonly_fields = ('created_at',)


# Registering the models
admin.site.register(User, UserAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(InstituteAdmin, InstituteAdminAdmin)
admin.site.register(Otp, OtpAdmin)
