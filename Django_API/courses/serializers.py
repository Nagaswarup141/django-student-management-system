"""courses/serializers.py"""
from rest_framework import serializers
from .models import Course

class CourseSerializer(serializers.ModelSerializer):
    enrolled_count = serializers.ReadOnlyField()
    class Meta:
        model  = Course
        fields = ['id','code','name','department','credits','instructor','semester','is_active','enrolled_count','created_at']
        read_only_fields = ['created_at']
