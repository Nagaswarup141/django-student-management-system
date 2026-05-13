"""fees/models.py"""
from django.db import models
from students.models import Student
from courses.models import Course

class PaymentMode(models.TextChoices):
    ONLINE = 'Online','Online Transfer'
    CASH   = 'Cash',  'Cash'
    DD     = 'DD',    'Demand Draft'
    CARD   = 'Card',  'Card'

class FeeRecord(models.Model):
    student      = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='fees')
    course       = models.ForeignKey(Course,  on_delete=models.CASCADE, related_name='fees')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=45000)
    paid_amount  = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    due_date     = models.DateField()
    payment_mode = models.CharField(max_length=10, choices=PaymentMode.choices, blank=True)
    semester     = models.CharField(max_length=20, default='Fall 2024')
    remarks      = models.TextField(blank=True)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['student','course','semester']
        ordering        = ['-created_at']

    def __str__(self):
        return f'{self.student.student_id} | {self.course.code} | {self.status}'

    @property
    def outstanding(self):
        return float(self.total_amount - self.paid_amount)

    @property
    def status(self):
        if self.paid_amount >= self.total_amount: return 'Paid'
        if self.paid_amount > 0:                  return 'Partial'
        return 'Pending'

    @property
    def payment_percentage(self):
        if not self.total_amount: return 0
        return round((float(self.paid_amount)/float(self.total_amount))*100, 1)
