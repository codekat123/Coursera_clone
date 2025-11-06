from rest_framework import permissions

class IsInstructor(permissions.BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'instructor')

class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'student')

class IsOwnerInstructor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return hasattr(request.user, 'instructor') and obj.instructor == request.user
