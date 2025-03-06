from django.urls import path 
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *
urlpatterns = format_suffix_patterns([
    path(''),
    path('<int:id>/'),
    path('course/<int:id>/'),
    path('course/<str:slug>/'),
])
