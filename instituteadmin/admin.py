from user.admin import UserAdmin
from django.contrib import admin
from .models import InstituteAdmin
from django.utils.translation import gettext_lazy as _

class InstituteAdminAdmin(UserAdmin):
    list_display = ('email', 'name', 'is_active', 'is_staff')

    fieldsets = UserAdmin.fieldsets + (
        (_("Institute Info"), {'fields': ('name', 'description', 'logo', 'details')}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (_("Institute Info"), {'fields': ('name', 'description', 'logo', 'details')}),
    )
    
    

admin.site.register(InstituteAdmin, InstituteAdminAdmin)