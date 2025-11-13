from rest_framework import serializers
from ..models.quiz import Quiz
from .question import QuestionSerializer


class QuizDetailSerializer(serializers.ModelSerializer):
     questions = QuestionSerializer(many=True)
     class Meta:
          model = Quiz
          fields = ['title','course','description','created_at']

class QuizListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ['id', 'title', 'course']

class QuizDetailSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    class Meta:
        model = Quiz
        fields = ['id', 'title', 'description', 'course', 'questions']

class QuizCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ['title', 'description', 'course']
        extra_kwargs = {
            'course': {'read_only': True}
        }

