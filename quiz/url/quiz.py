from django.urls import path
from ..views.quiz import (
    QuizCreateView,
    QuizListView,
    QuizRetrieveView,
    QuizUpdateView,
    QuizDestroyView,
)

urlpatterns = [
    path('courses/<slug:slug>/quizzes/create/', QuizCreateView.as_view(), name='quiz-create'),
    path('quizzes/', QuizListView.as_view(), name='quiz-list'),
    path('quizzes/<int:pk>/', QuizRetrieveView.as_view(), name='quiz-retrieve'),
    path('quizzes/<int:id>/update/', QuizUpdateView.as_view(), name='quiz-update'),
    path('quizzes/<int:id>/delete/', QuizDestroyView.as_view(), name='quiz-delete'),
]
