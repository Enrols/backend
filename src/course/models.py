from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from instituteadmin.models import InstituteAdmin
import constants
from datetime import timedelta
from preference.models import Tag, Location

def default_duration():
    return timedelta(weeks=2)

class Course(models.Model):
    class Meta:
        verbose_name_plural = 'Courses'
         
    class Types(models.TextChoices):
        ON_CAMPUS = 'ON_CAMPUS', 'Campus'
        ONLINE = 'ONLINE', 'Online',
        HYBRID = 'HYBRID', 'Hybrid'
    
    offered_by = models.ForeignKey(InstituteAdmin, null=True, on_delete=models.CASCADE, related_name='offered_courses')
    name = models.CharField(max_length=255)
    mode = models.CharField(max_length=20, choices=Types.choices, default=Types.ON_CAMPUS)
    description = models.TextField(default='')
    image = models.ImageField(upload_to=constants.IMAGE_UPLOAD_PATH, blank=True, null=True)
    # duration
    # batches[]
    syllabus = models.FileField(upload_to=constants.FILE_UPLOAD_PATH, blank=True, null=True)
    slug = models.CharField(max_length=20, null=False, default='', unique=True)
    # eligibiilty_criteria[]
    fee_amount = models.IntegerField(validators=[MinValueValidator(0)])
    fee_breakdown = models.FileField(upload_to=constants.FILE_UPLOAD_PATH, blank=True, null=True)
    tags = models.ManyToManyField(Tag, related_name='courses')
    # form_fields
    # documents_required
    
    def __str__(self):
        offered_by_name = self.offered_by.name if self.offered_by else 'N/A'
        return f"Course: {self.name} by {offered_by_name}"
    
class ApplicationFormField(models.Model):
    class Meta:
        verbose_name_plural = 'Application form fields'
    class FieldType(models.TextChoices):
        TEXT = 'TEXT', 'text'
        NUMBER = 'NUMBER', 'number'
        RADIO = 'RADIO', 'radio'
        DROPDOWN = 'DROPDOWN', 'dropdown'
        CHECKBOX = 'CHECKBOX', 'checkbox'
        
    field_name = models.CharField(max_length=255)
    field_type = models.CharField(max_length=20, choices=FieldType.choices, default=FieldType.TEXT)
    choices = models.CharField(max_length=255, blank=True, null=True, help_text="Enter values in comma separated format. Leave empty if not required (eg: 'Physics,Chemistry,Biology')")
    helper_text = models.CharField(max_length=255, help_text="Helper text for field information", default="")
    required = models.BooleanField(default=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="form_fields")
    
    def __str__(self):
        return f"{self.field_name} ({self.get_field_type_display()}) - {self.course.name}"
    
    
class RequiredDocument(models.Model):
    class Meta:
        verbose_name_plural = 'Required Documents'
        
    class FileTypes(models.TextChoices):
        IMAGE = 'IMAGE', 'image (png / jpg)'
        DOC = 'DOC', 'document (pdf)'
        
    file_name = models.CharField(max_length=255)
    file_type = models.CharField(max_length=20, choices=FileTypes.choices, default=FileTypes.IMAGE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='documents_required')    
class Duration(models.Model):
    class Meta:
        verbose_name_plural = 'Durations'
    
    hours = models.IntegerField(help_text="Enter duration in hours", default=0,validators=[MinValueValidator(0)])
    days = models.IntegerField(help_text="Enter duration in days", default=0, validators=[MinValueValidator(0)])
    weeks = models.IntegerField(help_text="Enter duration in weeks", default=2, validators=[MinValueValidator(0)])
    months = models.IntegerField(help_text="Enter duration in months", default=0, validators=[MinValueValidator(0)])
    years = models.IntegerField(help_text="Enter duration in years", default=0, validators=[MinValueValidator(0)])
    course = models.OneToOneField(Course,blank=False, null=False, on_delete=models.CASCADE, related_name='duration')

    def get_duration(self):
        return f"{self.years} years, {self.months} months, {self.weeks} weeks, {self.days} days, {self.hours} hours"

    def __str__(self):
        return f"Duration for course {self.course.name}: {self.years} years, {self.months} months, {self.weeks} weeks, {self.days} days, {self.hours} hours"


class EligibilityCriterion(models.Model):
    class Meta:
        verbose_name_plural = 'Eligibility Criteria'

    course = models.ForeignKey(Course, null=True, on_delete=models.CASCADE, related_name='eligibility_criteria')
    detail = models.CharField(max_length=255, blank=False, null=False)
    
    def __str__(self):
        return f"El. Cri. {self.detail}"  


class Batch(models.Model):
    class Meta:
        verbose_name_plural = 'Batches'
            
    course = models.ForeignKey(Course, null=True, on_delete=models.CASCADE, related_name='batches')
    location = models.ForeignKey(Location, null=True, on_delete=models.PROTECT, related_name='batches')
    commencement_date = models.DateField(null=True)
    discount = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(1)])
    
    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
    
    
    def __str__(self):
        course_name = self.course.name if self.course else "N/A"
        location_name = self.location.name if self.location else "N/A"
        return f"Batch for (Course: {course_name}) in (Location: {location_name})"
