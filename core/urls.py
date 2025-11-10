from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/',include('users.urls',namespace='users')),
    path('courses/',include('courses.urls',namespace='courses')),
    path('enrollments/',include('enrollments.urls',namespace='enrollments')),
]
