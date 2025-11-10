from django.db import models


class Subject(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True)

    class Meta:
        ordering = ["title"]

    def __str__(self) -> str:
        return str(self.title)
