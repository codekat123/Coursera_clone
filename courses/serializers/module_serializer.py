from rest_framework import serializers
from ..models import Module
from .content_serializer import ContentSerializer

class ModuleSerializer(serializers.ModelSerializer):
    contents = ContentSerializer(many=True, read_only=True)

    class Meta:
        model = Module
        fields = ['id', 'title', 'description', 'course', 'contents']
