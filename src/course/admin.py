from django.contrib import admin
from .models import Course, Batch, Duration, EligibilityCriterion, ApplicationFormField, RequiredDocument
from user.authentication import get_specific_user
from django import forms

class BatchInline(admin.TabularInline):
    model = Batch
    extra = 1

class EligibilityCriterionInline(admin.TabularInline):
    model = EligibilityCriterion
    extra = 1
    

class DurationInline(admin.TabularInline):
    model = Duration
    min_num = 1
    can_delete = False
    

class ApplicationFormFieldForm(forms.ModelForm):

    class Meta:
        model = ApplicationFormField
        fields = '__all__'

    def clean_choices(self):
        field_type = self.cleaned_data.get('field_type')
        choices = self.cleaned_data.get('choices', '')
        if field_type in ['RADIO', 'DROPDOWN', 'CHECKBOX']:
            if not choices:
                raise forms.ValidationError("Choices are required for radio, dropdown, and checkbox fields.")

            if not all(c.isalnum() for c in choices.split(',')):
                raise forms.ValidationError("Choices must be in the format: x,y,z,w (no spaces, only alphanumeric).")

        elif choices:
            raise forms.ValidationError("Choices are only application to fields of type 'radio' / 'checkbox' / 'dropdown'")

        return choices

class RequiredDocumentsForm(forms.ModelForm):
    class Meta:
        model = RequiredDocument
        fields = '__all__'
class ApplicationFormFieldInline(admin.TabularInline):
    """Inline form for ApplicationFormField in CourseAdmin."""
    model = ApplicationFormField
    form = ApplicationFormFieldForm
    extra = 1
    can_delete = True
        
class RequiredDocumentsInline(admin.TabularInline):
    """Inline form for Required documents"""
    model = RequiredDocument
    form = RequiredDocumentsForm
    extra = 1
    can_delete = True        
        
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'offered_by', 'mode', 'fee_amount', 'min_education_level')
    list_filter = ('mode', 'offered_by')
    search_fields = ('name', 'offered_by__email')  
    prepopulated_fields = {"slug": ("name",)}
    inlines = [BatchInline, EligibilityCriterionInline, DurationInline, ApplicationFormFieldInline, RequiredDocumentsInline, ]

    filter_horizontal = ('tags', 'relevant_interests')
    
    def save_related(self, request, form, formsets, change):
        """Save Duration object after saving Course object."""
        super().save_related(request, form, formsets, change)
        obj = form.instance
        obj.duration.save()

    def save_model(self, request, obj, form, change):
        """Automatically set offered_by to request.user for non-superusers."""
        if not request.user.is_superuser:
            institute = get_specific_user(request.user)
            obj.offered_by = institute
        super().save_model(request, obj, form, change)
    
    
    def get_queryset(self, request):
        """Restrict non-superusers to only their own courses."""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        
        institute = get_specific_user(request.user)
        return qs.filter(offered_by=institute)
    
    
    def get_fields(self, request, obj):
        fields = super().get_fields(request, obj)
        if request.user.is_superuser:
            return fields
        if 'offered_by' in fields:
            fields.remove('offered_by')
        return fields


class BatchAdmin(admin.ModelAdmin):
    list_display = ('course', 'location', 'commencement_date', 'discount')
    list_filter = ('course',)
    search_fields = ('course__name', 'location')

    def get_queryset(self, request):
        """Restrict non-superusers to only their own batches."""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        
        institute = get_specific_user(request.user)
        return qs.filter(course__in=institute.offered_courses.all())


class EligibilityCriterionAdmin(admin.ModelAdmin):
    list_display = ('course', 'detail')
    search_fields = ('course__name', 'detail')

    def get_queryset(self, request):
        """Restrict non-superusers to El. Cr. of their own courses only."""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        
        institute = get_specific_user(request.user)
        return qs.filter(course__in=institute.offered_courses.all())
   

class DurationAdmin(admin.ModelAdmin):
    list_display = ('course', 'years', 'months', 'weeks', 'days', 'hours' )
    search_fields = ('course__name', 'years', 'months', 'weeks', 'days', 'hours')

    def get_queryset(self, request):
        """Restrict non-superusers to Durations of their own courses only."""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        
        institute = get_specific_user(request.user)
        return qs.filter(course__in=institute.offered_courses.all())
 
   
admin.site.register(Course, CourseAdmin)
admin.site.register(Batch, BatchAdmin)
admin.site.register(EligibilityCriterion, EligibilityCriterionAdmin)
admin.site.register(Duration, DurationAdmin)