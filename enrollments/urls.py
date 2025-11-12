from django.urls import path
from .views import (
     EnrollmentCreateView,
     EnrollmentDestroyView
)

app_name = 'enrollments'

urlpatterns = [
     path('create/',EnrollmentCreateView.as_view(),name='enrollment-create'),
     path('delete/',EnrollmentDestroyView.as_view(),name='enrollment-delete'),
]