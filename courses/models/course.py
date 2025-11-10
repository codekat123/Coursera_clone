from django.db import models
from django.utils.text import slugify
from users.models import Student, Instructor
from .subject import Subject


class Course(models.Model):
    class Status(models.TextChoices):
        AVAILABLE = "AV", "Available"
        DERAFT = "DF", "Draft"

    instructor = models.ForeignKey(Instructor, related_name="courses_created", on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, related_name="courses", on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True, blank=True, null=True)
    overview = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=2, choices=Status, default=Status.AVAILABLE)
    price = models.DecimalField(max_digits=5,decimal_places=2)

    class Meta:
        ordering = ["-created"]

    def __str__(self) -> str:
        return str(self.title)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            counter = 0
            unique_slug = base_slug

            while Course.objects.filter(slug=unique_slug).exists():
                counter += 1
                unique_slug = f"{base_slug} - {counter}"

            self.slug = unique_slug
        super().save(*args, **kwargs)
