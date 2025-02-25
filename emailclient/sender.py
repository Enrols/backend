from django.core.mail import send_mail
from django.conf import settings

frontend_url = settings.FRONTEND_URL

def generate_reset_email(username: str, reset_link: str) -> str:
    return f"""\
Hi {username},

We received a request to reset your password. Click the link below to create a new password:

🔗 {reset_link}

This link is valid for the next 30 minutes. If you didn't request this, you can ignore this email.

For any issues, please contact our support team.

Best regards,  
Enrols
"""

def generate_verification_email(username: str, verification_link: str) -> str:
    return f"""\
Hi {username},

Thank you for signing up with Enrols! Please verify your email address by clicking the link below:

🔗 {verification_link}

If you did not create an account, you can ignore this email.

Best regards,  
Enrols
"""



def send_password_reset_email(user_email: str, username: str, reset_token: str):
    reset_link = f"{frontend_url}/reset-password?token={reset_token}"
    subject = "Reset Your Password"
    message = generate_reset_email(username, reset_link)

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [user_email],
        fail_silently=False,
    )
    


def send_verification_email(user_email: str, username: str, verification_token: str):
    verification_link = f"{frontend_url}/verify-email?token={verification_token}"
    subject = "Verify Your Email Address"
    message = generate_verification_email(username, verification_link)

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [user_email],
        fail_silently=False,
    )
