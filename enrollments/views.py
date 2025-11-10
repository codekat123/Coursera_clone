from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import ValidationError
from .serializers import EnrollmentSerializer
from .models import Enrollment
from courses.models import Course
from users.permissions import IsStudent

class EnrollmentCreateView(CreateAPIView):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsStudent]

    def perform_create(self, serializer):
        student = self.request.user
        course_id = self.kwargs.get('course_id')

        if not course_id:
            raise ValidationError({'detail': 'Missing course id.'})

        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            raise ValidationError({'detail': 'Course not found.'})

        if Enrollment.objects.filter(student=student, course=course).exists():
            raise ValidationError({'detail': 'Already enrolled in this course.'})

        serializer.save(student=student, course=course)
