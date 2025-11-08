from rest_framework import serializers
from ..models import Module
from .content import ContentSerializer

class ModuleListRetrieveSerializer(serializers.ModelSerializer):
    contents = ContentSerializer(many=True, read_only=True)

    class Meta:
        model = Module
        fields = ['id', 'title', 'description', 'course', 'contents']

class ModuleCreateUpdateSerializer(serializers.ModelSerializer):
    contents = ContentSerializer(many=True, read_only=True)
    course = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Module
        fields = ['id', 'title', 'description', 'course', 'contents']
