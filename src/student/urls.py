from django.urls import path 
from rest_framework.urlpatterns import format_suffix_patterns
from .views import LoginOtpView, LoginOtpVerifyView

urlpatterns = format_suffix_patterns([
    # path('register/'),
    # path('register/otp/'), 
    path('login/otp/', LoginOtpView.as_view(), name='token_obtain_otp'),
    path('login/otp/<str:token>', LoginOtpVerifyView.as_view(), name='verify_otp'),
    
])
