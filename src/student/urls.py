from django.urls import path 
from rest_framework.urlpatterns import format_suffix_patterns
from .views import LoginOtpView, LoginOtpVerifyView, RegisterView, RegisterOtpView, PhoneNumberVerifyView

urlpatterns = format_suffix_patterns([
    path('register/', RegisterView.as_view(), name='register_user'),
    path('register/otp/', RegisterOtpView.as_view(), name='reigster_otp'),
    path('register/otp/<str:token>', PhoneNumberVerifyView.as_view(), name='verify_phone_number'), 
    path('login/otp/', LoginOtpView.as_view(), name='token_obtain_otp'),
    path('login/otp/<str:token>', LoginOtpVerifyView.as_view(), name='verify_otp'),
])
