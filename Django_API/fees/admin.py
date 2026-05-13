from django.contrib import admin
from .models import FeeRecord

@admin.register(FeeRecord)
class FeeRecordAdmin(admin.ModelAdmin):
    list_display    = ['student','course','total_amount','paid_amount','status','due_date']
    list_filter     = ['semester','payment_mode']
    search_fields   = ['student__first_name','student__last_name','student__student_id']
    readonly_fields = ['created_at','updated_at']

    def status(self, obj):
        return obj.status
