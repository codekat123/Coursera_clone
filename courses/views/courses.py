from rest_framework.generics import CreateAPIView,UpdateAPIView,ListAPIView,DestroyAPIView,RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import ValidationError, PermissionDenied
from django.shortcuts import get_object_or_404
from rest_framework import filters
from ..models import Course, Subject
from users.models import Instructor
from ..serializers.course import CourseDetailSerializer,CourseListSerializer,CourseCreateUpdateSerializer
from users.permissions import IsInstructor
from django.core.cache import cache




class CourseCreateAPIView(CreateAPIView):
    """
    Allows instructors (polymorphic User subtype) to create courses under a given subject.
    """
    queryset = Course.objects.all()
    serializer_class = CourseCreateUpdateSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsInstructor]

    def perform_create(self, serializer):
        slug = self.kwargs.get("slug")
        if not slug:
            raise ValidationError({"detail": "Missing subject slug in URL."})

        subject = get_object_or_404(Subject, slug=slug)
        user = self.request.user

        if not isinstance(user, Instructor):
            raise ValidationError({"detail": "Only instructors can create courses."})

        serializer.save(subject=subject, instructor=user)


class CourseUpdateAPIView(UpdateAPIView):
    """
    Allows an instructor to update one of their own courses.
    Lookup is done via slug.
    """
    serializer_class = CourseCreateUpdateSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsInstructor]

    def get_object(self):
        slug = self.kwargs.get("slug")
        if not slug:
            raise ValidationError({"detail": "Missing course slug in URL."})

        course = get_object_or_404(Course, slug=slug,)


        if course.instructor != self.request.user:
            raise PermissionDenied({"detail": "You can only update your own courses."})

        return course
    
class CourseDestroyAPIView(DestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsInstructor]

    def get_object(self):
        slug = self.kwargs.get('slug')
        if not slug:
            raise ValidationError({'detail': 'Missing course slug in URL'})

        course = get_object_or_404(Course, slug=slug,instructor=self.request.user)
        return course

class CourseListAPIView(ListAPIView):
    serializer_class = CourseListSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "description"]
    ordering_fields = ["created_at", "rating"]

    def get_queryset(self):
        subject_slug = self.kwargs.get("slug")
        if not subject_slug:
            raise ValidationError({"detail": "Subject slug is required"})

        subject = get_object_or_404(Subject, slug=subject_slug)
        ids_cache_key = f"subject_{subject.slug}_course_ids"
        serialized_cache_key = f"subject_{subject.slug}_courses_page_1"


        page = self.request.query_params.get("page", "1")
        if page == "1":
            cached_data = cache.get(serialized_cache_key)
            if cached_data:

                self._cached_response = cached_data
                return Course.objects.none()  


        course_ids = cache.get(ids_cache_key)
        if course_ids:
            queryset = Course.objects.filter(id__in=course_ids).select_related("subject", "instructor")
        else:
            queryset = Course.objects.filter(subject=subject).select_related("subject", "instructor")
            cache.set(ids_cache_key, list(queryset.values_list("id", flat=True)), timeout=60 * 10)

        return queryset

    def list(self, request, *args, **kwargs):

        if hasattr(self, "_cached_response"):
            return self.get_paginated_response(self._cached_response)

        response = super().list(request, *args, **kwargs)


        page = request.query_params.get("page", "1")
        if page == "1":
            cache.set(
                f"subject_{self.kwargs.get('slug')}_courses_page_1",
                response.data["results"] if "results" in response.data else response.data,
                timeout=60 * 10,
            )

        return response

class CourseRetrieveAPIView(RetrieveAPIView):
    """
    Returns full course details including modules for public or enrolled access.
    """
    serializer_class = CourseDetailSerializer
    queryset = Course.objects.select_related("subject", "instructor").prefetch_related("modules")
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        slug = self.kwargs.get("slug")
        if not slug:
            raise ValidationError({"detail": "Missing course slug in URL."})

        course = get_object_or_404(self.queryset, slug=slug)
        return course