from django.db import models
from user.models import User
from utils import validate_details

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