from django.db import models
from .base import User


class Instructor(User):
    full_name = models.CharField(max_length=100)
    title = models.CharField(max_length=100, blank=True, null=True)
    specialization = models.CharField(max_length=100, blank=True, null=True)
    total_students = models.PositiveIntegerField(default=0)
    total_courses = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.username
