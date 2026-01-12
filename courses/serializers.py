from rest_framework import serializers
from .models import Course, Video
from accounts.models import CustomUser

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    videos = VideoSerializer(many=True, read_only=True)
    students = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Course
        fields = '__all__'
