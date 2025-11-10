from rest_framework.generics import (
    CreateAPIView, ListAPIView, RetrieveAPIView, DestroyAPIView
)
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import ValidationError, PermissionDenied
from django.shortcuts import get_object_or_404
from ..models import Content, Module
from ..serializers.content import ContentSerializer
from users.permissions import IsInstructor
from django.contrib.contenttypes.models import ContentType
from ..models import Module, Content, Text, File, Image, Video
from ..serializers.item import (
    TextSerializer,
    FileSerializer,
    ImageSerializer,
    VideoSerializer
)


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


ITEM_SERIALIZERS = {
    'text': TextSerializer,
    'file': FileSerializer,
    'image': ImageSerializer,
    'video': VideoSerializer
}


class CreateItemWithContentAPIView(CreateAPIView):
    """
    Creates both an Item (Text/File/Image/Video) and its Content link in one request.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsInstructor]

    def create(self, request, *args, **kwargs):
        item_type = request.data.get('type')
        module_id = request.data.get('module_id')
        item_data = request.data.get('data')

        if not item_type or item_type not in ITEM_SERIALIZERS:
            raise ValidationError({'detail': 'Invalid or missing item type.'})

        if not module_id:
            raise ValidationError({'detail': 'Module ID is required.'})

        module = get_object_or_404(Module, id=module_id)
        if module.course.instructor != request.user:
            raise PermissionDenied({'detail': 'You can only add content to your own modules.'})


        serializer_class = ITEM_SERIALIZERS[item_type]
        item_serializer = serializer_class(data=item_data)
        item_serializer.is_valid(raise_exception=True)
        item = item_serializer.save(instructor=request.user)


        content_type = ContentType.objects.get_for_model(item)
        content = Content.objects.create(
            module=module,
            content_type=content_type,
            object_id=item.id
        )

        return Response({
            'message': 'Item and content created successfully.',
            'content_id': content.id,
            'item': item_serializer.data
        })


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
