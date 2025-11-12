from django.urls import path
from ..views.answer import (
    StudentAnswerCreateView,
    GetScoreAPIView,
)

urlpatterns = [
    # Submit an answer to a specific question
    path('questions/<int:id>/answers/submit/', StudentAnswerCreateView.as_view(), name='answer-submit'),

    # Get the authenticated student's score summary for a quiz
    path('quizzes/<int:id>/score/', GetScoreAPIView.as_view(), name='quiz-score'),
]
