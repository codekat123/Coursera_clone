from rest_framework.generics import CreateAPIView,UpdateAPIView,ListAPIView,DestroyAPIView,RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import ValidationError, PermissionDenied
from django.shortcuts import get_object_or_404
from ..models import Course, Module
from ..serializers.module import ModuleListRetrieveSerializer,ModuleCreateUpdateSerializer
from users.permissions import IsInstructor


class ModuleCreateAPIView(CreateAPIView):
    """
    Allows an instructor to create a module under one of their own courses.
    The course is identified by its slug in the URL.
    """
    queryset = Module.objects.all()
    serializer_class = ModuleCreateUpdateSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsInstructor]

    def perform_create(self, serializer):
        slug = self.kwargs.get("slug")
        if not slug:
            raise ValidationError({"detail": "Missing course slug in URL."})

        course = get_object_or_404(Course, slug=slug)


        if course.instructor_id != self.request.user.id:
            raise PermissionDenied({"detail": "You are not allowed to add modules to this course."})

        serializer.save(course=course)




class ModuleUpdateAPIView(UpdateAPIView):
    """
    Allows an instructor to update one of their own modules.
    The module is looked up by its ID and verified through the course's instructor.
    """
    serializer_class = ModuleCreateUpdateSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsInstructor]

    def get_object(self):
        module_id = self.kwargs.get('id')
        if not module_id:
            raise ValidationError({'detail': 'Module ID must be included in the URL.'})

        return get_object_or_404(
            Module,
            id=module_id,
            course__instructor=self.request.user
        )

class ModuleDestroyAPIView(DestroyAPIView):
    """
    Allows an instructor to delete one of their own modules.
    Lookup is done via module ID, validated against the course's instructor.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsInstructor]

    def get_object(self):
        module_id = self.kwargs.get('id')
        if not module_id:
            raise ValidationError({'detail': 'Module ID must be included in the URL.'})

        module = get_object_or_404(Module, id=module_id)


        if module.course.instructor != self.request.user:
            raise PermissionDenied({'detail': 'You do not have permission to delete this module.'})

        return module
    
class ModuleListAPIView(ListAPIView):
    serializer_class = ModuleListRetrieveSerializer

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        if not slug:
            raise ValidationError({'detail': 'Missing course slug in URL'})

        course = get_object_or_404(Course, slug=slug)
        return (
            Module.objects
            .filter(course=course)
            .select_related('course')
            .prefetch_related('contents')
        )

class ModuleRetrieveAPIView(RetrieveAPIView):
    """
    Retrieve a single module by its ID (or slug if you have one).
    Includes related contents.
    """
    serializer_class = ModuleListRetrieveSerializer

    def get_object(self):
        module_id = self.kwargs.get("id")
        if not module_id:
            raise ValidationError({"detail": "Module ID must be included in the URL."})


        module = (
            Module.objects
            .select_related("course")
            .prefetch_related("contents")
            .filter(id=module_id)
            .first()
        )

        if not module:
            raise ValidationError({"detail": "Module not found."})

        return module