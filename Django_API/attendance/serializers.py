"""attendance/serializers.py"""
from rest_framework import serializers
from .models import Attendance

class AttendanceSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.full_name', read_only=True)
    student_code = serializers.CharField(source='student.student_id', read_only=True)
    course_code  = serializers.CharField(source='course.code', read_only=True)
    class Meta:
        model  = Attendance
        fields = ['id','student','student_name','student_code','course','course_code','date','status','remarks','marked_by','created_at']
        read_only_fields = ['created_at']
