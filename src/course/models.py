from django.db import models
from datetime import timedelta
from django.core.validators import MinValueValidator, MaxValueValidator
from instituteadmin.models import InstituteAdmin
import constants

def default_duration():
    return timedelta(weeks=2)


class Tag(models.Model):
    class Meta:
        verbose_name_plural = 'Tags'
        
    name = models.CharField(max_length=25, unique=True, null=False, default='default-tag')
    # courses[]
    def __str__(self):
        return f"Tag: {self.name}"
 
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
    # duration
    # batches[]
    syllabus = models.FileField(upload_to=constants.FILE_UPLOAD_PATH, blank=True, null=True)
    slug = models.CharField(max_length=20, null=False, default='', unique=True)
    # eligibiilty_criteria[]
    fee_amount = models.IntegerField(validators=[MinValueValidator(0)])
    fee_breakdown = models.FileField(upload_to=constants.FILE_UPLOAD_PATH, blank=True, null=True)
    tags = models.ManyToManyField(Tag, related_name='courses')
    
    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)    

    def __str__(self):
        offered_by_name = self.offered_by.name if self.offered_by else 'N/A'
        return f"Course: {self.name} by {offered_by_name}"
    
   
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
        return f"Duration: {self.years} years, {self.months} months, {self.weeks} weeks, {self.days} days, {self.hours} hours"

    def __str__(self):
        return f"Duration for course {self.course.name}: {self.years} years, {self.months} months, {self.weeks} weeks, {self.days} days, {self.hours} hours"


class EligibilityCriterion(models.Model):
    class Meta:
        verbose_name_plural = 'Eligibility Criteria'

    course = models.ForeignKey(Course, null=True, on_delete=models.CASCADE, related_name='eligibility_criteria')
    detail = models.TextField(blank=False, null=False)
    
    def __str__(self):
        return f"El. Cri. {self.detail}"
    
class Location(models.Model):
    class Meta:
        verbose_name_plural = 'Locations'
        
        
    name = models.CharField(max_length=255, unique=True, null=False)
    image = models.ImageField(upload_to=constants.IMAGE_UPLOAD_PATH)
    
    
    def __str__(self):
        return f"Location: {self.name}"


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
