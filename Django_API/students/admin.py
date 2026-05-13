"""students/admin.py"""
from django.contrib import admin
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display    = ['student_id','first_name','last_name','email','department','year','is_active','created_at']
    list_filter     = ['department','year','is_active','gender']
    search_fields   = ['first_name','last_name','email','student_id']
    readonly_fields = ['student_id','created_at','updated_at']
    ordering        = ['-created_at']
