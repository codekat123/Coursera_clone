from rest_framework import serializers
from ..models import Text, File, Image, Video

class TextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Text
        fields = ['id', 'title', 'instructor', 'content', 'created', 'updated']


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['id', 'title', 'instructor', 'file', 'created', 'updated']


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'title', 'instructor', 'image', 'created', 'updated']


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'title', 'instructor', 'video', 'created', 'updated']
