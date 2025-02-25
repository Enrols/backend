from rest_framework_simplejwt.authentication import JWTAuthentication
from user.models import User, Student, InstituteAdmin

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