from django.db import models
from .question import Question
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class Answer(models.Model):  # for MCQ choices
    text = models.CharField(max_length=255)
