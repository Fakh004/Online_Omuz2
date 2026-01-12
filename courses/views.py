from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Course, Video
from .serializers import CourseSerializer, VideoSerializer
from accounts.permissions import IsAdmin, IsTeacher, IsStudent

# -------------------
# Курсы
# -------------------
class CourseListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)

    def post(self, request):
        if request.user.role not in ['admin', 'teacher']:
            return Response({'detail': 'Нет прав на создание курса'}, status=status.HTTP_403_FORBIDDEN)
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(teacher=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseEnrollAPIView(APIView):
    permission_classes = [IsAuthenticated, IsStudent]

    def post(self, request, course_id):
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({'detail': 'Курс не найден'}, status=status.HTTP_404_NOT_FOUND)
        course.students.add(request.user)
        return Response({'message': f'Вы записаны на курс {course.title}'}, status=status.HTTP_200_OK)



class VideoCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.role not in ['admin', 'teacher']:
            return Response({'detail': 'Нет прав на добавление видео'}, status=status.HTTP_403_FORBIDDEN)
        serializer = VideoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
