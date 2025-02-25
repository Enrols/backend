from rest_framework.urlpatterns import format_suffix_patterns   
from django.urls import path 
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from .views import LoginOtpView, ForgotPasswordView, ResetPasswordView, VerifyEmailView, VerifyEmailTokenView, LoginOtpVerifyView, ProfileView

urlpatterns = format_suffix_patterns([
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/otp/', LoginOtpView.as_view(), name='token_obtain_otp'),
    path('login/otp/<str:token>', LoginOtpVerifyView.as_view(), name='verify_otp'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('verify-token/', TokenVerifyView.as_view(), name='token_verify'),
    path('send-verify-email/', VerifyEmailView.as_view(), name='send_verify_email'),
    path('verify-email/<str:token>/', VerifyEmailTokenView.as_view(), name='verify_email'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('reset-password/<str:token>/', ResetPasswordView.as_view(), name='reset_password'),
    path('profile/', ProfileView.as_view(), name='profile_view')
])
