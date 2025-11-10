from django.db import models
from .course import Course


class Module(models.Model):
    course = models.ForeignKey(Course, related_name="modules", on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    description = models.TextField(blank=True)

    def __str__(self) -> str:
        return str(self.title)
