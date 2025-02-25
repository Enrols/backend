from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import constants
from .utils import generate_otp
from django.utils import timezone
from .utils import format_phone_number, validate_details
class UserManager(BaseUserManager):
    """ Manager for custom user """

    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        
        email = self.normalize_email(email)
        
                
        user = self.model(
            email=email,
        )
        user.set_password(password)
        user.save(using=self._db)
        
        return user
    
    def create_superuser(self, email, password=None):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True 
        user.save(using=self._db)
        
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """ Custom user model """
    class Types(models.TextChoices):
        STUDENT = 'STUDENT', 'Student'
        INSTITUTE_ADMIN = 'INSTITUTE_ADMIN', 'InstituteAdmin'
    
    email = models.EmailField(unique=True)
    account_type = models.CharField(max_length=20, choices=Types.choices, default=Types.STUDENT)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    
    is_student = models.BooleanField(default=True)
    is_institute = models.BooleanField(default=False)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    
    def as_specific(self):
        """ Returns the specific model instance (Student or InstituteAdmin) """
        if self.account_type == self.Types.STUDENT:
            return Student.objects.get(pk=self.pk)
        elif self.account_type == self.Types.INSTITUTE_ADMIN:
            return InstituteAdmin.objects.get(pk=self.pk)
        return self 
    
    def __str__(self):
        return f"<< User: {self.email} >>"
    
    
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

class InstituteManager(models.Manager):
    def create_user(self, email, name, description, password=None, **other_fields):
        if not email:
            raise ValueError("Email should be provided")
        
        email = self.normalize_email(email)
        
        user = self.model(
            email=email,
            name=name,
            description=description,
            **other_fields
        )
        
        user.set_password(password)
        user.is_staff = True
        user.save() 
        
        return user 
    
    def get_queryset(self , *args,  **kwargs): 
        queryset = super().get_queryset(*args , **kwargs) 
        queryset = queryset.filter(account_type=User.Types.INSTITUTE_ADMIN) 
        return queryset 
    
    

class InstituteAdmin(User):
    objects = InstituteManager()
    
    name = models.CharField(max_length=255, unique=False)
    description = models.TextField(blank=True, null=False, default="")
    logo = models.ImageField(upload_to='public/media/', blank=True, null=True)
    details = models.JSONField(default=list, validators=[validate_details])

    
    def save(self , *args , **kwargs):
        if not self.id or self.id == None: 
            self.account_type = User.Types.INSTITUTE_ADMIN 
        self.is_student = False 
        self.is_institute = True 
        return super().save(*args , **kwargs)
    
    
    def __str__(self):
        return f"<< Inst Admin: {self.email} >>"
        
        
    
    
    
    
class Otp(models.Model):
    """ OTP Model"""
    
    phone_number = models.CharField(max_length=20, unique=False)
    otp = models.CharField(max_length=6, unique=False, default=generate_otp())
    created_at = models.DateTimeField(default=timezone.now)
    def is_valid(self) -> bool:
        return (timezone.now()) > self.created_at + constants.OTP_EXP_TIME
        
    def get_expiration_time(self):
        return self.created_at + constants.OTP_EXP_TIME
    
    def __str__(self):
        return f"<< OTP: {self.phone_number}, {self.otp}, {'(expired)' if self.exp > timezone.now() else ''} >>"
    
    
    
    