from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
# Register your models here.
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'full_name', 'phone_number', 'is_staff', 'is_active',)
    list_filter = ('is_staff', 'is_active',)
    ordering = ('email',)
    search_fields = ('email', 'full_name', 'phone_number',)
    
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("full_name", "phone_number")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
        ("Important Dates", {"fields": ("last_login", "date_joined")}),
    )
    
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "full_name", "phone_number", "password1", "password2", "is_staff", "is_active"),
        }),
    )
    
    
admin.site.register(User, CustomUserAdmin)