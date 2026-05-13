"""courses/models.py"""
from django.db import models
from students.models import Department

class Course(models.Model):
    code       = models.CharField(max_length=20, unique=True)
    name       = models.CharField(max_length=200)
    department = models.CharField(max_length=10, choices=Department.choices)
    credits    = models.PositiveSmallIntegerField(default=3)
    instructor = models.CharField(max_length=100)
    semester   = models.CharField(max_length=20, default='Fall 2024')
    is_active  = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['code']

    def __str__(self):
        return f'{self.code} — {self.name}'

    @property
    def enrolled_count(self):
        from students.models import Student
        return Student.objects.filter(is_active=True, department=self.department).count()
