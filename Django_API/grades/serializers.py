"""grades/serializers.py"""
from rest_framework import serializers
from .models import Grade

class GradeSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.full_name',  read_only=True)
    student_code = serializers.CharField(source='student.student_id', read_only=True)
    course_code  = serializers.CharField(source='course.code',        read_only=True)
    course_name  = serializers.CharField(source='course.name',        read_only=True)
    percentage   = serializers.ReadOnlyField()
    letter_grade = serializers.ReadOnlyField()
    grade_points = serializers.ReadOnlyField()
    total_marks  = serializers.ReadOnlyField()

    class Meta:
        model  = Grade
        fields = ['id','student','student_name','student_code','course','course_code','course_name',
                  'mid_term','final_exam','assignment','total_marks','percentage','letter_grade',
                  'grade_points','semester','remarks','created_at','updated_at']
        read_only_fields = ['created_at','updated_at']
