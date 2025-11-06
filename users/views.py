from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Student, Instructor
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated 
from .serializers import (
    StudentRegisterSerializer,
    InstructorRegisterSerializer
)

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


class RegisterAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        role = request.data.get("role")
    
        serializer_map = {
            "student": StudentRegisterSerializer,
            "instructor": InstructorRegisterSerializer
        }
        serializer_class = serializer_map.get(role)
        if not serializer_class:
            return Response(
                {"error": "Invalid role. Must be 'student' or 'instructor'."},
                status=status.HTTP_400_BAD_REQUEST
            )
    
        serializer = serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        tokens = get_tokens_for_user(user)
    
        return Response({
            "message": f"{role.capitalize()} registered successfully.",
            "username": user.username,
            "tokens": tokens
        }, status=status.HTTP_201_CREATED)



class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        refresh_token = request.data.get('refresh_token')
        if not refresh_token:
            return Response()
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message':'logged out successfully'},status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response({'error':'invalid or expire token'},status=status.HTPP_400_BAD_REQUEST)
