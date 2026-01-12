from django.urls import path
from .views import CourseListCreateAPIView, CourseEnrollAPIView, VideoCreateAPIView

urlpatterns = [
    path('courses/', CourseListCreateAPIView.as_view(), name='courses'),
    path('courses/<int:course_id>/enroll/', CourseEnrollAPIView.as_view(), name='course-enroll'),
    path('videos/', VideoCreateAPIView.as_view(), name='add-video'),
]
