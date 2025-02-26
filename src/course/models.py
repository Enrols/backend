from django.db import models
from datetime import timedelta
from django.core.validators import MinValueValidator, MaxValueValidator
from instituteadmin.models import InstituteAdmin

def default_duration():
    return timedelta(weeks=2)


class Tag(models.Model):
    name = models.CharField(25, unique=True)
    # courses[]
    pass


class Course(models.Model):
    class Types(models.TextChoices):
        ON_CAMPUS = 'ON_CAMPUS', 'Campus'
        ONLINE = 'ONLINE', 'Online',
        HYBRID = 'HYBRID', 'Hybrid'
    
    offered_by = models.ForeignKey(InstituteAdmin, null=True, on_delete=models.CASCADE, related_name='offered_courses')
    name = models.CharField(max_length=255)
    mode = models.CharField(max_length=20, choices=Types.choices, default=Types.ON_CAMPUS)
    description = models.TextField(default='')
    duration = models.DurationField(default=default_duration)
    # batches[]
    syllabus = models.FileField(upload_to='../../public/media', blank=True, null=True)
    slug = models.CharField(max_length=20, null=False, default='')
    # eligibiilty_criteria[]
    fee_amount = models.IntegerField(validators=[MinValueValidator(0)])
    fee_breakdown = models.FileField(upload_to='../../public/media', blank=True, null=True)
    tags = models.ManyToManyField(Tag, related_name='courses')
    
    
    REQUIRED_FIELDS = ['name']
    

class EligibilityCriteria(models.Model):
    course = models.ForeignKey(Course, null=True, on_delete=models.CASCADE, related_name='eligibility_criteria')
    detail = models.TextField(blank=False, null=False)
    
    REQUIRED_FIELDS = ['detail']

class Batch(models.Model):
    course = models.ForeignKey(Course, null=True, on_delete=models.CASCADE, related_name='batches')
    location = models.CharField(max_length=255)
    commencement_date = models.DateField(null=True)
    discount = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(1)])
    
    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
    


class WishList(models.Model):
    pass
