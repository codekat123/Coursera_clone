from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from ..models import Content, Text, File, Image, Video
from .item import (
    TextSerializer,
    FileSerializer,
    ImageSerializer,
    VideoSerializer
)

class ContentSerializer(serializers.ModelSerializer):
    item = serializers.SerializerMethodField()
    content_type = serializers.SlugRelatedField(
        slug_field='model', queryset=ContentType.objects.all()
    )
    class Meta:
        model = Content
        fields = ['id', 'module', 'content_type', 'object_id', 'item']

    def get_item(self, obj):
        """Return the nested serialized data for the specific content type."""
        if isinstance(obj.item, Text):
            return TextSerializer(obj.item).data
        elif isinstance(obj.item, File):
            return FileSerializer(obj.item).data
        elif isinstance(obj.item, Image):
            return ImageSerializer(obj.item).data
        elif isinstance(obj.item, Video):
            return VideoSerializer(obj.item).data
        return None
