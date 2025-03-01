from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import TagListView, TagStreamListView, TagSkillListView, TagExamListView, InterestListView, LocationListView, EducationLevelListView


urlpatterns = format_suffix_patterns([
    path('tag/streams/',TagStreamListView.as_view(),name='tag-streams'),
    path('tag/exams/',TagExamListView.as_view(),name='tag-exams'),
    path('tag/skills/',TagSkillListView.as_view(),name='tag-skills'),
    path('interests/',InterestListView.as_view(), name='interests'),
    path('education-levels/',EducationLevelListView.as_view(),name='education-levels'),
    path('locations/',LocationListView.as_view(),name='locations'),
    path('tags',TagListView.as_view(),name='tags'),
])
