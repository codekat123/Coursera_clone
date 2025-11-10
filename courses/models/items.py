from django.db import models
from users.models import Instructor


class ItemBase(models.Model):
    instructor = models.ForeignKey(Instructor, related_name="%(class)s_related", on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return str(self.title)


class Text(ItemBase):
    content = models.TextField()


class File(ItemBase):
    file = models.FileField(upload_to="files")


class Image(ItemBase):
    image = models.ImageField(upload_to="images")


class Video(ItemBase):
    video = models.URLField()
