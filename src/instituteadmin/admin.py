from user.admin import UserAdmin
from django.contrib import admin
from .models import InstituteAdmin, Detail
from django.utils.translation import gettext_lazy as _



class DetailAdminInline(admin.TabularInline):
    model = Detail 
    extra = 1
class InstituteAdminAdmin(UserAdmin):
    list_display = ('email', 'name',)
    list_filter = []
    inlines = [DetailAdminInline]
    
    fieldsets = (
        (_("User Information"), {"fields": ("email", "password")}),
        (_("Institute Info"), {'fields': ('name', 'description', 'logo')}),
        (_("Important Dates"), {"fields": ("date_joined",)}),
    )

    add_fieldsets = (
        (_("Create User"), {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2"),
        }),
        (_("Institute Info"), {'fields': ('name', 'description', 'logo')}),
    )

    
    

admin.site.register(InstituteAdmin, InstituteAdminAdmin)
