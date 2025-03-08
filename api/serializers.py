from rest_framework import serializers
from .models import Course  # Import Course model

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'  # Includes all fields from Course model
