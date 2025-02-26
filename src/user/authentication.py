from rest_framework_simplejwt.authentication import JWTAuthentication
from user.models import User
from student.models import Student
from instituteadmin.models import InstituteAdmin
from rest_framework.permissions import BasePermission

def get_specific_user(user):
    """Return the correct subclass instance based on account_type."""
    if not user or not user.is_authenticated:
        return user
    if user.account_type == User.Types.STUDENT:
        try:
            return Student.objects.get(pk=user.pk)
        except Student.DoesNotExist:
            return user
    elif user.account_type == User.Types.INSTITUTE_ADMIN:
        try:
            return InstituteAdmin.objects.get(pk=user.pk)
        except InstituteAdmin.DoesNotExist:
            return user
    return user

class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        auth_result = super().authenticate(request)
        if auth_result is None:
            return None
        user, token = auth_result

        specific_user = get_specific_user(user)
        return (specific_user, token)
    
    
class IsStudent(BasePermission):
    """
    Custom permission to permit only students
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        
        return request.user.is_superuser or request.user.is_student
    

class IsEmailVerified(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        if request.user.is_superuser:
            return True
        return request.user.is_student and request.user.email_verified
    
    
class IsPhoneVerified(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        if request.user.is_superuser:
            return True
        return request.user.is_student and request.user.phone_number_verified
    

    
class IsInstituteAdmin(BasePermission):
    """
    Custom permission to permit only students
    """
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        
        return request.user.is_superuser or request.user.is_institute