from rest_framework import serializers
from ..models import Course
from .subject_serializer import SubjectSerializer
from .module_serializer import ModuleSerializer

class CourseSerializer(serializers.ModelSerializer):
    modules = ModuleSerializer(many=True, read_only=True)
    subject = SubjectSerializer(read_only=True)
    instructor = serializers.StringRelatedField()

    class Meta:
        model = Course
        fields = [
            'id', 'title', 'slug', 'overview', 'subject',
            'instructor', 'status', 'created', 'modules'
        ]
        read_only_fields = ['slug', 'created']
