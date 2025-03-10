from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *

urlpatterns = format_suffix_patterns([
    path('recommended/', RecommendedCoursesView.as_view(), name='recommended-courses'),
])
