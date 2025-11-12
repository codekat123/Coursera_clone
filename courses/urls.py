from django.urls import path
from rest_framework.routers import DefaultRouter
from .views.subject import SubjectViewSet
app_name='courses'



router = DefaultRouter()
router.register(r"subjects", SubjectViewSet, basename="subject")

from .url.course import urlpatterns as course_urlpatterns
from .url.module import urlpatterns as module_urlpatterns
from .url.content import urlpatterns as content_urlpatterns

urlpatterns = router.urls + course_urlpatterns + module_urlpatterns + content_urlpatterns
