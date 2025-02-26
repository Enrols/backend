from django.db import models
from utils import format_phone_number
from user.models import User
from course.models import Tag, Course

class StudentManager(models.Manager):
    def create_user(self, email, full_name, phone_number, password=None, **other_fields):
        if not email:
            raise ValueError("Users must have an email address")
        
        email = self.normalize_email(email)
        phone_number = format_phone_number(phone_number=phone_number)
        
        if not phone_number:
            raise ValueError("Phone number should exist and should be valid")
        
        user = self.model(
            email=email,
            full_name=full_name,
            phone_number=phone_number
            **other_fields
        )
        
        user.set_password(password)
        user.save()
        return user
    
    def get_queryset(self , *args,  **kwargs): 
        queryset = super().get_queryset(*args , **kwargs) 
        queryset = queryset.filter(account_type=User.Types.STUDENT) 
        return queryset  
    
class Student(User):
    objects = StudentManager()
    
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, unique=True)
    selected_tags = models.ManyToManyField(Tag)
    wishlist = models.ManyToManyField(Course)
    
    email_verified = models.BooleanField(default=False)
    phone_number_verified = models.BooleanField(default=False)
    
    REQUIRED_FIELDS = ['full_name', 'phone_number']
    
    def save(self , *args , **kwargs):
        if not self.id or self.id == None: 
            self.account_type = User.Types.STUDENT 
        self.is_student = True 
        self.is_institute = False 
        return super().save(*args , **kwargs)
    
    def __str__(self):
        return f"<< Student: {self.email} >>"