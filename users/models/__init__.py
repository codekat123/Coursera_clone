from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,Group, Permission
from polymorphic.models import PolymorphicModel
from .model_manager import CustomUserManager

class User(AbstractBaseUser):
     username = models.CharField(unique=True,db_index=True,max_length=30)
     is_active = models.BooleanField(default=True)
     is_staff = models.BooleanField(default=False)
     date_joined = models.DateTimeField(auto_now_add=True)
     groups = models.ManyToManyField(Group, related_name="custom_user_groups", blank=True)
     user_permissions = models.ManyToManyField(Permission, related_name="custom_user_permissions", blank=True)

     USERNAME_FIELD = 'username'

     objects = CustomUserManager()

     def __str__(self):
          return self.username



class Student(User):
    full_name = models.CharField(max_length=100)
    level = models.CharField(max_length=50, blank=True, null=True)  
    date_of_birth = models.DateField(blank=True, null=True)
    enrolled_count = models.PositiveIntegerField(default=0)  

    def __str__(self):
     return self.username


class Instructor(User):
    full_name = models.CharField(max_length=100)
    title = models.CharField(max_length=100, blank=True, null=True)
    specialization = models.CharField(max_length=100, blank=True, null=True)
    total_students = models.PositiveIntegerField(default=0)
    total_courses = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.username
    