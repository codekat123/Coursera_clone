from rest_framework import serializers 
from ..models import Answer,StudentAnswer

class AnswerSerializer(serializers.ModelSerializer):
     class Meta:
          model = Answer
          fields = ['text']


class StudentAnswerdetailSerializer(serializers.ModelSerializer):
     selected_answer = AnswerSerializer(many=True)
     class Meta:
          model = StudentAnswer
          fields = '__all__'

class StudentAnswerCreateSerializer(serializers.ModelSerializer):
     class Meta:
          model = StudentAnswer
          fields = ['text_answer','bool_answer','selected_answer']