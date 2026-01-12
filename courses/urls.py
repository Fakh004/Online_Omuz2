from django.urls import path
from .views import CourseListCreateAPIView, CourseDetailAPIView, CourseEnrollAPIView

urlpatterns = [
    path('courses/', CourseListCreateAPIView.as_view(), name='courses'),
    path('courses/<int:course_id>/', CourseDetailAPIView.as_view(), name='course-detail'),
    path('courses/<int:course_id>/enroll/', CourseEnrollAPIView.as_view(), name='course-enroll'),
]
