from django.urls import path 
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *
urlpatterns = format_suffix_patterns([
    path('', ApplicationsListView.as_view(), name='applications-list'),
    path('<int:id>/', ApplicationView.as_view(), name='application'),
    path('<int:id>/upload-docs/<int:doc_id>/', ApplicationUploadDocView.as_view(), name='upload-related-docs'),
    path('course/<int:id>/', ApplicationByCourseView.as_view(), name='application-by-course'),
    path('course/<str:slug>/', ApplicationByCourseSlugView.as_view(), name='application-by-course-slug'),
])
