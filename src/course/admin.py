from django.contrib import admin
from .models import Course, Batch, Duration, EligibilityCriterion
from user.authentication import get_specific_user

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
        
class CourseAdmin(admin.ModelAdmin):
    # form = CourseDurationForm
    list_display = ('name', 'offered_by', 'mode', 'fee_amount')
    list_filter = ('mode', 'offered_by')
    search_fields = ('name', 'offered_by__email')  
    prepopulated_fields = {"slug": ("name",)}
    inlines = [BatchInline, EligibilityCriterionInline, DurationInline]

    filter_horizontal = ('tags', )

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