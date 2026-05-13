"""grades/models.py"""
from django.db import models
from students.models import Student
from courses.models import Course

class Grade(models.Model):
    student    = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='grades')
    course     = models.ForeignKey(Course,  on_delete=models.CASCADE, related_name='grades')
    mid_term   = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    final_exam = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    assignment = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    semester   = models.CharField(max_length=20, default='Fall 2024')
    remarks    = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['student','course','semester']
        ordering        = ['-created_at']

    def __str__(self):
        return f'{self.student.student_id} | {self.course.code} | {self.letter_grade}'

    @property
    def total_marks(self):
        return float(self.mid_term + self.final_exam + self.assignment)

    @property
    def percentage(self):
        return round((self.total_marks / 120) * 100, 2)

    @property
    def letter_grade(self):
        p = self.percentage
        if p >= 90: return 'A+'
        if p >= 80: return 'A'
        if p >= 70: return 'B+'
        if p >= 60: return 'B'
        if p >= 50: return 'C'
        return 'F'

    @property
    def grade_points(self):
        return {'A+':10,'A':9,'B+':8,'B':7,'C':6,'F':0}.get(self.letter_grade, 0)
