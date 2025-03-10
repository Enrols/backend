from rest_framework.views import APIView
from course.models import Course 
from course.serializers import CourseSerializer
from user.authentication import IsStudent
from rest_framework.response import Response
from django.db.models import Q, Count
import random
from rest_framework import status


class RecommendedCoursesView(APIView):
    permission_classes = [IsStudent]
    response_serializer = CourseSerializer
    def get(self, request):
        student = request.user
        
        matching_courses = Course.objects.filter(
            Q(tags__in=student.selected_tags.all()) |
            Q(relevant_interests__in=student.interests.all()) |
            Q(min_education_level=student.current_education_level)
        ).distinct()
        
        scored_courses = matching_courses.annotate(
            tag_match=Count('tags', filter=Q(tags__in=student.selected_tags.all())),
            interest_match=Count('relevant_interests', filter=Q(relevant_interests__in=student.interests.all())),
            edu_match=Count('min_education_level', filter=Q(min_education_level__level__lte=student.current_education_level.level))
        )
        
        for course in scored_courses:
            course.match_score = (course.tag_match * 3) + (course.interest_match * 2) + (course.edu_match * 1)
        
        sorted_courses = sorted(scored_courses, key=lambda x: x.match_score, reverse=True)

        top_courses = sorted_courses[:10]
        random.shuffle(top_courses)

        serializer = CourseSerializer(top_courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
            
        

