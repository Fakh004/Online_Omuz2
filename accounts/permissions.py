from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    message = "Доступ только для админов."
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.role == 'admin' or request.user.is_superuser)

class IsTeacher(BasePermission):
    message = "Доступ только для учителей."
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'teacher'

class IsStudent(BasePermission):
    message = "Доступ только для студентов."
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'student' and not request.user.is_superuser
