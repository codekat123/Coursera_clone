from django.db import models
from .base import User


class Student(User):
    full_name = models.CharField(max_length=100)
    level = models.CharField(max_length=50, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    enrolled_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.username
