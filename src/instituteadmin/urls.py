from django.urls import path 
from rest_framework.urlpatterns import format_suffix_patterns
from .views import InstituteCourseListView, InstituteDetailView

urlpatterns = format_suffix_patterns([
    path('<int:id>/', InstituteDetailView.as_view(), name='institute-details'),
    path('<int:id>/courses/',InstituteCourseListView.as_view(), name='institute-courses')
])
