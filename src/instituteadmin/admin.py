from user.admin import UserAdmin
from django.contrib import admin
from .models import InstituteAdmin, Detail
from django.utils.translation import gettext_lazy as _



class DetailAdminInline(admin.TabularInline):
    model = Detail 
    extra = 1
class InstituteAdminAdmin(UserAdmin):
    list_display = ('email', 'name', 'is_active', 'is_staff')
    inlines = [DetailAdminInline]

    fieldsets = UserAdmin.fieldsets + (
        (_("Institute Info"), {'fields': ('name', 'description', 'logo')}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (_("Institute Info"), {'fields': ('name', 'description', 'logo')}),
    )
    
    

admin.site.register(InstituteAdmin, InstituteAdminAdmin)
