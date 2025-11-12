from django.shortcuts import get_object_or_404
from rest_framework.generics import CreateAPIView,DestroyAPIView,UpdateAPIView,RetrieveAPIView,ListAPIView
from ..serializers.quiz import QuizListSerializer, QuizDetailSerializer, QuizCreateSerializer
from ..models import Quiz
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from users.permissions import IsInstructor
from rest_framework.exceptions import ValidationError, PermissionDenied
from courses.models.course import Course


class QuizCreateView(CreateAPIView):
     queryset = Quiz.objects.all()
     serializer_class = QuizCreateSerializer
     authentication_classes = [JWTAuthentication]
     permission_classes = [IsAuthenticated, IsInstructor]

     def perform_create(self,serializer):
          slug_course = self.kwargs['slug']
          if not slug_course:
               raise ValidationError({'detail':'missing course id'})

          course = get_object_or_404(Course,slug=slug_course)
          if course.instructor != self.request.user:
               raise PermissionDenied({'error': 'You are not allowed to create a quiz for this course.'})

          serializer.save(course=course)

class QuizUpdateView(UpdateAPIView):
    serializer_class = QuizCreateSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsInstructor]
    queryset = Quiz.objects.all()
    
    def get_object(self):
        quiz_id = self.kwargs.get('id')
        if not quiz_id:
            raise ValidationError({'detail': 'Missing quiz id.'})
        
        quiz = get_object_or_404(Quiz, id=quiz_id)
        
        if quiz.course.instructor != self.request.user:
            raise PermissionDenied({'error': 'You are not allowed to update this quiz.'})
        
        return quiz


class QuizListView(ListAPIView):
    serializer_class = QuizListSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Quiz.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        course_id = self.request.query_params.get("course_id")
        if course_id:
            queryset = queryset.filter(course_id=course_id)
        return queryset



class QuizRetrieveView(RetrieveAPIView):
    serializer_class = QuizDetailSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Quiz.objects.all()



class QuizUpdateView(UpdateAPIView):
    serializer_class = QuizCreateSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsInstructor]
    queryset = Quiz.objects.all()

    def get_object(self):
        quiz_id = self.kwargs.get('id')
        quiz = get_object_or_404(Quiz, id=quiz_id)
        if quiz.course.instructor != self.request.user:
            raise PermissionDenied({'error': 'You are not allowed to update this quiz.'})
        return quiz



class QuizDestroyView(DestroyAPIView):
    serializer_class = QuizDetailSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsInstructor]
    queryset = Quiz.objects.all()

    def get_object(self):
        quiz_id = self.kwargs.get('id')
        quiz = get_object_or_404(Quiz, id=quiz_id)
        if quiz.course.instructor != self.request.user:
            raise PermissionDenied({'error': 'You are not allowed to delete this quiz.'})
        return quiz
