"""fees/serializers.py"""
from rest_framework import serializers
from .models import FeeRecord

class FeeRecordSerializer(serializers.ModelSerializer):
    student_name       = serializers.CharField(source='student.full_name',  read_only=True)
    student_code       = serializers.CharField(source='student.student_id', read_only=True)
    course_code        = serializers.CharField(source='course.code',        read_only=True)
    status             = serializers.ReadOnlyField()
    outstanding        = serializers.ReadOnlyField()
    payment_percentage = serializers.ReadOnlyField()

    class Meta:
        model  = FeeRecord
        fields = ['id','student','student_name','student_code','course','course_code',
                  'total_amount','paid_amount','outstanding','payment_percentage','status',
                  'due_date','payment_mode','semester','remarks','created_at','updated_at']
        read_only_fields = ['created_at','updated_at']

class RecordPaymentSerializer(serializers.Serializer):
    amount       = serializers.DecimalField(max_digits=10, decimal_places=2)
    payment_mode = serializers.ChoiceField(choices=['Online','Cash','DD','Card'])
    transaction_id = serializers.CharField(required=False, allow_blank=True)
