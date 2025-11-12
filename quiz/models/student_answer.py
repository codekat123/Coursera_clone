from django.db import models
from .question import Question
from .mcq import Answer
from users.models.student import Student





class StudentAnswer(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_answer = models.ForeignKey(Answer, on_delete=models.SET_NULL, null=True, blank=True)
    text_answer = models.CharField(max_length=255, blank=True, null=True)
    bool_answer = models.BooleanField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student} → {self.question}"