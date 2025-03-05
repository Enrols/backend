from django.db import models
from student.models import Student
from course.models import Course, ApplicationFormField, Batch
import constants
from django.utils import timezone

class ApplicationFormResponseField(models.Model):
    form_details = models.ForeignKey(ApplicationFormField, on_delete=models.CASCADE)
    value_text = models.CharField(max_length=255, blank=True)
    value_file = models.FileField(upload_to=constants.FILE_UPLOAD_PATH, blank=True)
    value_number = models.FloatField(blank=True)

class Application(models.Model):
    class Status(models.TextChoices):
        UNDER_REVIEW = 'UNDER_REVIEW', 'Under review'
        REVIEWED = 'REVIEWED', 'reviewed'
        REJECTED = 'REJECTED', 'rejected'
        PAID = 'REQUEST_PAYMENT', 'request payment'
        ACCEPTED = 'ACCEPTED', 'accepted'
        
    full_name = models.CharField(255, blank=False, null=False)
    phone_number = models.CharField(255, blank=False, null=False)
    email = models.EmailField(null=False, blank=False)
    date_of_birth = models.DateField(null=False, blank=False)
    
    form_data = models.ManyToManyField(ApplicationFormResponseField)
    
    applied_by = models.ForeignKey(Student, null=True, blank=True, on_delete=models.CASCADE, related_name="applications")
    course = models.ForeignKey(Course, null=True, blank=True, on_delete=models.CASCADE)    
    batch_selected = models.ForeignKey(Batch, null=True, blank=True)
    
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.UNDER_REVIEW)
    submitted_on = models.DateField(default=timezone.now)
    # transaction_details


class Transaction(models.Model):
    application = models.ForeignKey(Application, on_delete=models.DO_NOTHING, related_name='transaction_details')
    
    # other details to be added later when payment is implemented 

    