from rest_framework import serializers
from ..models import Course
from .subject import SubjectSerializer
from .module import ModuleSerializer

class CourseDetailSerializer(serializers.ModelSerializer):
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



class CourseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'title', 'slug', 'overview', 'subject', 'instructor']



class CourseCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['title', 'overview', 'status']

