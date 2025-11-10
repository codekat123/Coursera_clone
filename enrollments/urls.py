from django.urls import path
from .views import EnrollmentCreateView

app_name = 'enrollments'

urlpatterns = [
     path('',EnrollmentCreateView.as_view(),name='enrollment-create'),
]