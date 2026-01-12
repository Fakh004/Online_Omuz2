from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser

class RegisterAPIView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        role = request.data.get("role", "student")  # по умолчанию student

        if not username or not password:
            return Response({"detail": "Username и password обязательны"}, status=status.HTTP_400_BAD_REQUEST)

        # Если username = admin, создаём суперпользователя
        if username.lower() == "admin":
            user = CustomUser.objects.create_superuser(username=username, password=password, role="admin")
        else:
            user = CustomUser.objects.create_user(username=username, password=password, role=role)

        return Response({
            "message": "User created",
            "username": user.username,
            "role": user.role
        }, status=status.HTTP_201_CREATED)


from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

class LoginAPIView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"detail": "Username и password обязательны"}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)
        if not user:
            return Response({"detail": "Неверный username или password"}, status=status.HTTP_401_UNAUTHORIZED)

        token, created = Token.objects.get_or_create(user=user)
        role = "admin" if user.is_superuser else user.role

        return Response({
            "message": "Login successful",
            "username": user.username,
            "role": role,
            "token": token.key
        }, status=status.HTTP_200_OK)

class LogoutAPIView(APIView):
    def post(self, request):
        token_key = request.META.get('HTTP_AUTHORIZATION')
        if token_key and token_key.startswith('Token '):
            token_key = token_key.split(' ')[1]
            try:
                token = Token.objects.get(key=token_key)
                token.delete()
                return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
            except Token.DoesNotExist:
                return Response({"detail": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Token not provided"}, status=status.HTTP_400_BAD_REQUEST)