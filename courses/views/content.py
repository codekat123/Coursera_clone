from rest_framework.generics import (
    CreateAPIView, ListAPIView, RetrieveAPIView, DestroyAPIView
)
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import ValidationError, PermissionDenied
from django.shortcuts import get_object_or_404
from ..models import Content, Module
from ..serializers.content import ContentSerializer
from users.permissions import IsInstructor


class ContentListAPIView(ListAPIView):
    """
    List all content items under a specific module.
    """
    serializer_class = ContentSerializer

    def get_queryset(self):
        module_id = self.kwargs.get('module_id')
        if not module_id:
            raise ValidationError({'detail': 'Module ID is required.'})

        module = get_object_or_404(Module, id=module_id)
        return Content.objects.filter(module=module).select_related('content_type')


class ContentRetrieveAPIView(RetrieveAPIView):
    """
    Retrieve a single content object by its ID.
    """
    serializer_class = ContentSerializer

    def get_object(self):
        content_id = self.kwargs.get('id')
        if not content_id:
            raise ValidationError({'detail': 'Content ID must be provided.'})

        content = get_object_or_404(
            Content.objects.select_related('content_type', 'module'),
            id=content_id
        )
        return content


class ContentCreateAPIView(CreateAPIView):
    """
    Allows an instructor to add content to one of their modules.
    The module ID must be provided in the URL.
    """
    serializer_class = ContentSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsInstructor]

    def perform_create(self, serializer):
        module_id = self.kwargs.get('module_id')
        if not module_id:
            raise ValidationError({'detail': 'Module ID must be included in the URL.'})

        module = get_object_or_404(Module, id=module_id)

        if module.course.instructor != self.request.user:
            raise PermissionDenied({'detail': 'You can only add content to your own modules.'})

        serializer.save(module=module)


class ContentDestroyAPIView(DestroyAPIView):
    """
    Allows an instructor to delete one of their own content items.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsInstructor]

    def get_object(self):
        content_id = self.kwargs.get('id')
        if not content_id:
            raise ValidationError({'detail': 'Content ID must be provided.'})

        content = get_object_or_404(Content, id=content_id)

        if content.module.course.instructor != self.request.user:
            raise PermissionDenied({'detail': 'You are not allowed to delete this content.'})

        return content
