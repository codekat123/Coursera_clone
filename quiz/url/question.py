from django.urls import path
from ..views.question import (
    QuestionListView,
    QuestionRetrieveView,
    QuestionCreateView,
    QuestionUpdateView,
    QuestionDestroyView,
)

urlpatterns = [
    path('quizzes/<int:id>/questions/', QuestionListView.as_view(), name='question-list'),
    path('questions/<int:id>/', QuestionRetrieveView.as_view(), name='question-retrieve'),
    path('questions/create/', QuestionCreateView.as_view(), name='question-create'),
    path('questions/<int:id>/update/', QuestionUpdateView.as_view(), name='question-update'),
    path('questions/<int:id>/delete/', QuestionDestroyView.as_view(), name='question-delete'),
]
