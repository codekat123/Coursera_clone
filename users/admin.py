from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin
from .models import User, Student, Instructor


@admin.register(User)
class UserAdmin(PolymorphicParentModelAdmin, BaseUserAdmin):
    """Admin panel for the base User model (handles polymorphism)."""
    base_model = User
    child_models = [Student, Instructor]  
    list_display = ("username", "is_active", "is_staff")
    search_fields = ("username",)
    ordering = ("-date_joined",)
    list_filter = ("is_active", "is_staff", "date_joined")
    fieldsets = (
        ("User Info", {"fields": ("username", "password")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "groups", "user_permissions")}),
        ("Important Dates", {"fields": ("date_joined",)}),
    )


@admin.register(Student)
class StudentAdmin(PolymorphicChildModelAdmin):
    """Admin panel for Student model."""
    base_model = Student
    list_display = ("username", "full_name", "is_active", "date_joined")
    search_fields = ("username", "full_name")
    ordering = ("-date_joined",)
    list_filter = ("full_name", "is_active")
    fieldsets = (
        ("Student Info", {"fields": ("username", "full_name")}),
        ("Permissions", {"fields": ("is_active",)}),
        ("Important Dates", {"fields": ("date_joined",)}),
    )


@admin.register(Instructor)
class TeacherAdmin(PolymorphicChildModelAdmin):
    """Admin panel for Teacher model."""
    base_model = Instructor
    list_display = ("username", "full_name", "is_active", "date_joined")
    search_fields = ("username", "full_name")
    ordering = ("-date_joined",)
    list_filter = ("full_name", "is_active")
    fieldsets = (
        ("Teacher Info", {"fields": ("username", "full_name")}),
        ("Permissions", {"fields": ("is_active",)}),
        ("Important Dates", {"fields": ("date_joined",)}),
    )
