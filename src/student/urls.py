from django.urls import path 
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *

urlpatterns = format_suffix_patterns([
    path('education-level/',StudentEducationLevelView.as_view(),name='student-education-level'),
    path('tags/',StudentTagListView.as_view(),name='student-tags'),
    path('interests/',StudentInterestListView.as_view(),name='student-interests'),
    path('preferred-locations/',StudentLocationListView.as_view(),name='student-preferredlocations'),
    path('wishlist/',StudentWishListView.as_view(),name='student-wishlist'),
    path('wishlist/<int:course_id>', StudentWishListUpdateView.as_view(), name='student-wishlist-update')
])
