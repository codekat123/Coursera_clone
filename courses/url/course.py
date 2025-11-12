from django.urls import path
from ..views.courses import (
    CourseCreateAPIView,
    CourseUpdateAPIView,
    CourseDestroyAPIView,
    CourseListAPIView,
    CourseRetrieveAPIView,
)

urlpatterns = [
    path(
        "subjects/<slug:slug>/courses/",
        CourseListAPIView.as_view(),
        name="course-list",
    ),
    path(
        "subjects/<slug:slug>/courses/create/",
        CourseCreateAPIView.as_view(),
        name="course-create",
    ),
    path(
        "courses/<slug:slug>/update/",
        CourseUpdateAPIView.as_view(),
        name="course-update",
    ),
    path(
        "courses/<slug:slug>/delete/",
        CourseDestroyAPIView.as_view(),
        name="course-delete",
    ),
    path(
        "course/<slug:slug>/retrieve",
        CourseRetrieveAPIView.as_view(),
        name="course-retrieve",
    ),
]
