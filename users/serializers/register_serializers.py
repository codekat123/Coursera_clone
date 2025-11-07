from rest_framework import serializers
from ..models import Student, Instructor


class StudentRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = Student
        fields = [
            "username",
            "password",
            "full_name",
            "level",
            "date_of_birth",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        return Student.objects.create_user(**validated_data)


class InstructorRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = Instructor
        fields = [
            "username",
            "password",
            "full_name",
            "title",
            "specialization",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        return Instructor.objects.create_user(**validated_data)
