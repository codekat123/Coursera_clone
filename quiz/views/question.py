from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    UpdateAPIView,
    DestroyAPIView,
)
from ..serializers import QuestionSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import PermissionDenied,ValidationError
from django.shortcuts import get_object_or_404
from ..models import Question,Quiz
from users.permissions import IsInstructor

class QuestionListView(ListAPIView):
    serializer_class = QuestionSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        quiz_id = self.kwargs['id']
        quiz = get_object_or_404(Quiz,id=quiz_id)
        return Question.objects.filter(quiz=quiz)


class QuestionRetrieveView(RetrieveAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    lookup_field = 'id'
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


class QuestionCreateView(CreateAPIView):
    serializer_class = QuestionSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsInstructor]

    def perform_create(self, serializer):
        quiz = serializer.validated_data['quiz']
        if quiz.course.instructor != self.request.user:
            raise PermissionDenied({'error': 'You cannot add a question to another instructor’s quiz.'})
        serializer.save()


class QuestionUpdateView(UpdateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    lookup_field = 'id'
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsInstructor]
    
    def get_object(self):
        question_id = self.kwargs.get('id')
        if not question_id:
            raise ValidationError({'detail': 'Missing question ID.'})

        question = get_object_or_404(Question, id=question_id)

        if question.quiz.course.instructor != self.request.user:
            raise PermissionDenied({
                'error': 'You do not own this question'
            })
        return question

class QuestionDestroyView(DestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    lookup_field = 'id'
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsInstructor]
    def get_object(self):
        question_id = self.kwargs.get('id')
        if not question_id:
            raise ValidationError({'detail': 'Missing question ID.'})

        question = get_object_or_404(Question, id=question_id)

        
        if question.quiz.course.instructor != self.request.user:
            raise PermissionDenied({
                'error': 'You do not own this question'
            })
        return question