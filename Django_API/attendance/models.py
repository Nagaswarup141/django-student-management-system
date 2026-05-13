"""attendance/models.py"""
from django.db import models
from students.models import Student
from courses.models import Course

class AttendanceStatus(models.TextChoices):
    PRESENT = 'Present','Present'
    ABSENT  = 'Absent', 'Absent'
    LATE    = 'Late',   'Late'

class Attendance(models.Model):
    student    = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance')
    course     = models.ForeignKey(Course,  on_delete=models.CASCADE, related_name='attendance')
    date       = models.DateField()
    status     = models.CharField(max_length=10, choices=AttendanceStatus.choices, default='Present')
    remarks    = models.CharField(max_length=200, blank=True)
    marked_by  = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['student','course','date']
        ordering        = ['-date']

    def __str__(self):
        return f'{self.student.student_id} | {self.course.code} | {self.date} | {self.status}'
