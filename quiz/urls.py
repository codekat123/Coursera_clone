from django.urls import path

app_name = 'quiz'

from .url.quiz import urlpatterns as quiz_urlpatterns
from .url.question import urlpatterns as question_urlpatterns
from .url.answer import urlpatterns as answer_urlpatterns

urlpatterns = quiz_urlpatterns + question_urlpatterns + answer_urlpatterns