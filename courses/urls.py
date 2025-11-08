from django.urls import path
from rest_framework.routers import DefaultRouter
from .views.subject import SubjectViewSet
from .views.courses import (
    CourseCreateAPIView,
    CourseUpdateAPIView,
    CourseDestroyAPIView,
    CourseListAPIView,
    CourseRetrieveAPIView,
)

from .views.modules import (
    ModuleCreateAPIView,
    ModuleUpdateAPIView,
    ModuleDestroyAPIView,
    ModuleListAPIView,
    ModuleRetrieveAPIView,
)

from .views.content import (
    ContentListAPIView,
    ContentRetrieveAPIView,
    ContentCreateAPIView,
    ContentDestroyAPIView
)
app_name = "courses"


router = DefaultRouter()
router.register(r"subjects", SubjectViewSet, basename="subject")

urlpatterns = router.urls


urlpatterns += [

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
         name='course-retrieve'
    ),

    path(
        "courses/<slug:slug>/modules/",
        ModuleListAPIView.as_view(),
        name="module-list",
    ),

    path(
        "courses/<slug:slug>/modules/create/",
        ModuleCreateAPIView.as_view(),
        name="module-create",
    ),


    path(
        "modules/<int:id>/retrieve/",
        ModuleRetrieveAPIView.as_view(),
        name="module-retrieve",
    ),


    path(
        "modules/<int:id>/update/",
        ModuleUpdateAPIView.as_view(),
        name="module-update",
    ),


    path(
        "modules/<int:id>/delete/",
        ModuleDestroyAPIView.as_view(),
        name="module-delete",
    ),
    path('modules/<int:module_id>/contents/', ContentListAPIView.as_view(), name='content-list'),
    path('modules/<int:module_id>/contents/create/', ContentCreateAPIView.as_view(), name='content-create'),
    path('contents/<int:id>/', ContentRetrieveAPIView.as_view(), name='content-retrieve'),
    path('contents/<int:id>/delete/', ContentDestroyAPIView.as_view(), name='content-delete'),
]
