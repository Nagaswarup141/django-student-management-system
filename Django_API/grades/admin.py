from django.contrib import admin
from .models import Grade

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display    = ['student','course','mid_term','final_exam','assignment','semester']
    list_filter     = ['semester','course']
    search_fields   = ['student__first_name','student__last_name','student__student_id']
    readonly_fields = ['created_at','updated_at']
