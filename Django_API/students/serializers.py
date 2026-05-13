"""students/serializers.py"""
from rest_framework import serializers
from .models import Student

class StudentSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()
    class Meta:
        model  = Student
        fields = ['id','student_id','first_name','last_name','full_name','email','phone',
                  'department','year','gender','date_of_birth','address','photo','is_active','created_at','updated_at']
        read_only_fields = ['student_id','created_at','updated_at']

class StudentListSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()
    class Meta:
        model  = Student
        fields = ['id','student_id','full_name','first_name','last_name','email','department','year','is_active']
