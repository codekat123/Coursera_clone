from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from ..serializers.register_serializers import (
    StudentRegisterSerializer,
    InstructorRegisterSerializer,
)
from ..utils.tokens import get_tokens_for_user


class RegisterAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    serializer_map = {
        "student": StudentRegisterSerializer,
        "instructor": InstructorRegisterSerializer,
    }

    def post(self, request, *args, **kwargs):
        role = request.data.get("role")
        serializer_class = self.serializer_map.get(role)

        if not serializer_class:
            return Response(
                {"error": "Invalid role. Must be 'student' or 'instructor'."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        tokens = get_tokens_for_user(user)

        return Response(
            {
                "message": f"{role.capitalize()} registered successfully.",
                "username": user.username,
                "tokens": tokens,
            },
            status=status.HTTP_201_CREATED,
        )
