from django.urls import path
from ..views.modules import (
    ModuleCreateAPIView,
    ModuleUpdateAPIView,
    ModuleDestroyAPIView,
    ModuleListAPIView,
    ModuleRetrieveAPIView,
)

urlpatterns = [
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
]
