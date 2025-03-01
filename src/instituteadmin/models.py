from django.db import models
from user.models import User
from utils import validate_details
import constants

# Create your models here.
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
    class Meta:
        verbose_name_plural = 'Institute Admins'
        
        
    objects = InstituteManager()
    
    name = models.CharField(max_length=255, unique=False)
    description = models.TextField(blank=True, null=False, default="")
    logo = models.ImageField(upload_to=constants.IMAGE_UPLOAD_PATH, blank=True, null=True)
    # details = models.JSONField(default=list, validators=[validate_details])

    
    def save(self , *args , **kwargs):
        if not self.id or self.id == None: 
            self.account_type = User.Types.INSTITUTE_ADMIN 
        self.is_student = False 
        self.is_institute = True 
        self.is_staff = True
        return super().save(*args , **kwargs)
    
    
    def __str__(self):
        return f"Inst Admin: {self.email}"
    
class Detail(models.Model):
    class Meta:
        verbose_name_plural = 'Details'
        
        
    detail = models.CharField(max_length=100, unique=False, null=False, blank=False)
    info = models.CharField(max_length=255, blank=False, null=False, unique=False)
    admin = models.ForeignKey(InstituteAdmin, on_delete=models.CASCADE, null=True, blank=True, related_name='details') # delete details if InstitueAdmin deleted
    
    def __str__(self):
        return f"{{ '{self.detail}': '{self.info}' }}"
    