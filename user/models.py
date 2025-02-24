from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    """ Manager for custom user """

    def create_user(self, email, phone_number, full_name, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not phone_number:
            raise ValueError("Users must have a phone number")
        
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            phone_number=phone_number,
            full_name=full_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        
        return user
    
    def create_superuser(self, email, phone_number, full_name, password=None):
        user = self.create_user(email, phone_number, full_name, password)
        user.is_staff = True
        user.is_superuser = True 
        user.save(using=self._db)
        
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """ Custom user model """
    
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, unique=True)
    
    email_verified = models.BooleanField(default=False)
    phone_number_verified = models.BooleanField(default=False)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'phone_number']
    
    def __str__(self):
        return f"<< User: {self.email} >>"
    
    
    