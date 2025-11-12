from django.db import models
from .quiz import Quiz

class Question(models.Model):
    QUESTION_TYPES = [
        ('mcq', 'Multiple Choice'),
        ('true_false', 'True/False'),
        ('short', 'Short Answer'),
    ]

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES)
    correct_answer_text = models.CharField(max_length=255, blank=True, null=True)
    correct_answer_bool = models.BooleanField(blank=True, null=True)

    def __str__(self):
        return self.text

