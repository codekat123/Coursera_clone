from rest_framework import serializers
from ..models import Course
from .subject import SubjectSerializer
from .module import ModuleListRetrieveSerializer

class CourseDetailSerializer(serializers.ModelSerializer):
    modules = ModuleListRetrieveSerializer(many=True, read_only=True)
    subject = SubjectSerializer(read_only=True)
    instructor = serializers.StringRelatedField()

    class Meta:
        model = Course
        fields = [
            'id', 'title', 'slug', 'overview', 'subject',
            'instructor', 'status', 'created', 'modules','price',
        ]
        read_only_fields = ['slug', 'created']



class CourseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'title', 'slug', 'overview', 'subject', 'instructor','price']



class CourseCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['title', 'overview', 'status','price']

