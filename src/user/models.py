from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
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

    def __str__(self):
        return f"<< User: {self.email} >>"
