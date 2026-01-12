from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import Course
from .serializers import CourseSerializer
from accounts.permissions import IsAdmin, IsTeacher, IsStudent

# GET /courses/ and POST /courses/ (create)
@method_decorator(csrf_exempt, name='dispatch')
class CourseListCreateAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if not (request.user.role in ['admin', 'teacher'] or request.user.is_superuser):
            return Response({"detail": "Нет доступа для создания курса"}, status=status.HTTP_403_FORBIDDEN)

        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_exempt, name='dispatch')
class CourseDetailAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, course_id):
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({'detail': 'Курс не найден'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CourseSerializer(course)
        return Response(serializer.data, status=status.HTTP_200_OK)

@method_decorator(csrf_exempt, name='dispatch')
class CourseEnrollAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsStudent]

    def post(self, request, course_id):
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({'detail': 'Курс не найден'}, status=status.HTTP_404_NOT_FOUND)

        course.students.add(request.user)
        return Response({'message': f'Вы записаны на курс {course.title}'}, status=status.HTTP_200_OK)
