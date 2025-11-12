from ..models import StudentAnswer
from rest_framework.generics import CreateAPIView
from ..serializers import StudentAnswerCreateSerializer,StudentAnswerdetailSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import PermissionDenied,ValidationError
from users.permissions import IsInstructor
from django.shortcuts import get_object_or_404
from ..models import Question
from rest_framework.views import APIView
from django.db.models import Count, Q
from rest_framework.response import Response



class StudentAnswerCreateView(CreateAPIView):
    queryset = StudentAnswer.objects.all()
    serializer_class = StudentAnswerCreateSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        question_id = self.kwargs.get('id')
        if not question_id:
            raise ValidationError({'detail': 'Missing question ID.'})

        question = get_object_or_404(Question, id=question_id)
        student = self.request.user

        text_answer = serializer.validated_data.get('text_answer')
        bool_answer = serializer.validated_data.get('bool_answer')


        is_correct = (
            (question.correct_answer_text and text_answer == question.correct_answer_text) or
            (question.correct_answer_bool is not None and bool_answer == question.correct_answer_bool)
        )

        serializer.save(question=question, student=student, is_correct=is_correct)

class GetScoreAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        student = request.user

        if not StudentAnswer.objects.filter(quiz_id=id, student=student).exists():
            return Response({'detail': 'No answers found for this quiz.'}, status=404)

        total_questions = Question.objects.filter(quiz_id=id).count()

        summary = (
            StudentAnswer.objects
            .filter(quiz_id=id, student=student)
            .aggregate(
                correct_answers=Count('id', filter=Q(is_correct=True)),
                incorrect_answers=Count('id', filter=Q(is_correct=False)),
            )
        )
        summary['total_questions'] = total_questions
        summary['score_percent'] = (
            (summary['correct_answers'] / total_questions) * 100
            if total_questions > 0 else 0
        )

        return Response(summary, status=200)

