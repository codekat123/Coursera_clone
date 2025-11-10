from django.db import models
from courses.models.course import Course
from users.models.student import Student


class Enrollment(models.Model):
     course = models.ForeignKey(Course,on_delete=models.CASCADE,related_name='course_enrollments')
     student = models.ForeignKey(Student,on_delete=models.CASCADE,related_name='student_enrollments')
     progress = models.FloatField(default=0.0)