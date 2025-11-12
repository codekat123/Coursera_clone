from django.urls import path
from ..views.content import (
    ContentListAPIView,
    ContentRetrieveAPIView,
    CreateItemWithContentAPIView,
    ContentDestroyAPIView,
)

urlpatterns = [
    path('modules/<int:module_id>/contents/', ContentListAPIView.as_view(), name='content-list'),
    path('contents/create/', CreateItemWithContentAPIView.as_view(), name='content-create'),
    path('contents/<int:id>/', ContentRetrieveAPIView.as_view(), name='content-retrieve'),
    path('contents/<int:id>/delete/', ContentDestroyAPIView.as_view(), name='content-delete'),
]
