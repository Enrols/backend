from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *

urlpatterns = format_suffix_patterns([
    path('',CourseListView.as_view(),name='course-list'),
    path('<int:id>/',CourseDetailView.as_view(),name='course-detail'),
    path('<str:slug>/', CourseDetailSlugView.as_view(), name='course-detail-slug'),
    path('<int:id>/batches/',CourseBatchesListView.as_view(),name='course-batches'),
    path('<str:slug>/batches/', CourseBathcesListSlugView.as_view(), name='course-batches-slug'),

    path('<int:id>/form-details/', CourseFormDetailsListView.as_view(), name='course-form-details'),
    path('<str:slug>/form-details/', CourseFormDetailsListSlugView.as_view(), name='course-form-details-slug'),

    path('<int:id>/docs/', CourseReqDocsListView.as_view(), name='course-req-docs'),
    path('<str:slug>/docs/', CourseReqDocsListSlugView.as_view(), name='course-req-docs-slug'),
])
