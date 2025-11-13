from rest_framework import permissions
from users.models import Instructor, Student

class IsInstructor(permissions.BasePermission):
    def has_permission(self, request, view):
        return isinstance(request.user, Instructor)

class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        return isinstance(request.user, Student)

class IsOwnerInstructor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return isinstance(request.user, Instructor) and getattr(obj, 'instructor_id', None) == request.user.id
