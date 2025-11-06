from rest_framework import serializers
from .models import User, Student, Instructor


# ---- Base Serializer ---- #
class BaseUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ["id", "username", "password", "is_active", "date_joined"]
        read_only_fields = ["is_active", "date_joined"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class StudentRegisterSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        model = Student
        fields = BaseUserSerializer.Meta.fields + [
            "full_name",
            "level",
            "date_of_birth",
        ]

    def create(self, validated_data):
        return Student.objects.create_user(**validated_data)

class InstructorRegisterSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        model = Instructor
        fields = BaseUserSerializer.Meta.fields + [
            "full_name",
            "title",
            "specialization",
        ]

    def create(self, validated_data):
        return Instructor.objects.create_user(**validated_data)
