from django.urls import path 
from rest_framework.urlpatterns import format_suffix_patterns
from .views import StudentOnlyTestView, InstituteOnlyTestView, AnonTestView, AuthedView
urlpatterns = format_suffix_patterns([
    path('students-only/', StudentOnlyTestView.as_view()),
    path('institutes-only/', InstituteOnlyTestView.as_view()),
    path('any-auth/', AuthedView.as_view()),
    path('everyone/', AnonTestView.as_view()),
])
