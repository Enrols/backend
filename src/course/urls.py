from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *

urlpatterns = format_suffix_patterns([
    path('',CourseListView.as_view(),name='course-list'),
    path('<int:id>/',CourseDetailView.as_view(),name='course-detail'),
    path('<int:id>/locations',CourseLocationListView.as_view(),name='course-locations'),
])
