from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from ..models import Subject
from ..serializers.subject import SubjectSerializer
from users.permissions import IsInstructor


class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            permission_classes = [IsAuthenticated, IsInstructor]
        elif self.action in ["list", "retrieve"]:
            permission_classes = [AllowAny]  
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
