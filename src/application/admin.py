from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Application, ApplicationFormResponseField, DocumentUpload, Transaction
from django.shortcuts import redirect
from django.utils.html import format_html
from django.contrib import messages
from django.urls import path, reverse

class ApplicationFormResponseFieldInline(admin.TabularInline):
    model = ApplicationFormResponseField
    extra = 0
    readonly_fields = ('get_field_name', 'get_value',)
    fields = ('get_field_name', 'get_value', )

    def get_field_name(self, obj):
        return obj.form_details.field_name
    
    def get_value(self, obj):
        field_type = obj.form_details.field_type
        return obj.value_number if field_type == 'NUMBER' else obj.value_text

    get_value.short_description = "Value"
    get_field_name.short_description = "Field Name"

class DocumentUploadInline(admin.TabularInline):
    model = DocumentUpload
    extra = 0


class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone_number', 'course', 'status', 'submitted_on', 'updated_on', 'approve_reject_buttons',)
    list_filter = ('status', 'submitted_on', 'course')
    search_fields = ('full_name', 'email', 'phone_number', 'applied_by__full_name', 'course__name')
    readonly_fields = ('submitted_on', 'updated_on')
    
    change_form_template = 'admin/application_change_form_template.html'

    inlines = [ApplicationFormResponseFieldInline, DocumentUploadInline]

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return self.readonly_fields
        else:  # Assume institute admins are non-superusers
            return [field.name for field in self.model._meta.fields]
    
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
    
    actions = ['approve_application', 'reject_application']

    def approve_application(self, request, queryset):
        updated_count = queryset.update(status=Application.Status.ACCEPTED)
        self.message_user(request, f"{updated_count} application(s) approved.", messages.SUCCESS)

    def reject_application(self, request, queryset):
        updated_count = queryset.update(status=Application.Status.REJECTED)
        self.message_user(request, f"{updated_count} application(s) rejected.", messages.WARNING)

    approve_application.short_description = "Approve selected applications"
    reject_application.short_description = "Reject selected applications"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:application_id>/change/approve/', self.admin_site.admin_view(self.approve_view), name='approve_application'),
            path('<int:application_id>/change/reject/', self.admin_site.admin_view(self.reject_view), name='reject_application'),
        ]
        return custom_urls + urls

    def approve_view(self, request, application_id):
        application = Application.objects.get(id=application_id)
        application.status = Application.Status.ACCEPTED
        application.save()
        self.message_user(request, "Application approved.", messages.SUCCESS)
        return redirect(request.META.get('HTTP_REFERER', 'admin:index'))

    def reject_view(self, request, application_id):
        application = Application.objects.get(id=application_id)
        application.status = Application.Status.REJECTED
        application.save()
        self.message_user(request, "Application rejected.", messages.WARNING)
        return redirect(request.META.get('HTTP_REFERER', 'admin:index'))

    def approve_reject_buttons(self, obj):
        return format_html(
            '<a class="button" href="{}">Approve</a> &nbsp; <a class="button" style="color:red;" href="{}">Reject</a>',
            f"{obj.id}/change/approve/",
            f"{obj.id}/change/reject/",
        )
    
    approve_reject_buttons.allow_tags = True
    approve_reject_buttons.short_description = "Actions"


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('application',)
    readonly_fields = ('application',)

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return []
        return self.readonly_fields

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser


admin.site.register(Application, ApplicationAdmin)
admin.site.register(Transaction, TransactionAdmin)