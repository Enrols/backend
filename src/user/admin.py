from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User

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
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser", "groups")}),
        (_("Important Dates"), {"fields": ("date_joined",)}),
    )

    add_fieldsets = (
        (_("Create User"), {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2"),
        }),
    )

    readonly_fields = ('date_joined',)





# Registering the models
admin.site.register(User, UserAdmin)
