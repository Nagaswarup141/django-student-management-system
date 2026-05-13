from django.db import models

class Department(models.TextChoices):
    CS  = 'CS',  'Computer Science'
    EE  = 'EE',  'Electrical Engineering'
    ME  = 'ME',  'Mechanical Engineering'
    BBA = 'BBA', 'Business Administration'

class Gender(models.TextChoices):
    MALE   = 'Male',   'Male'
    FEMALE = 'Female', 'Female'
    OTHER  = 'Other',  'Other'

class Student(models.Model):
    student_id    = models.CharField(max_length=20, unique=True, editable=False)
    first_name    = models.CharField(max_length=100)
    last_name     = models.CharField(max_length=100)
    email         = models.EmailField(unique=True)
    phone         = models.CharField(max_length=20, blank=True)
    department    = models.CharField(max_length=10, choices=Department.choices)
    year          = models.PositiveSmallIntegerField(choices=[(i, f'Year {i}') for i in range(1, 5)])
    gender        = models.CharField(max_length=10, choices=Gender.choices, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    address       = models.TextField(blank=True)
    photo         = models.ImageField(upload_to='students/', null=True, blank=True)
    is_active     = models.BooleanField(default=True)
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.student_id:
            last = Student.objects.order_by('id').last()
            num  = (last.id + 1) if last else 1
            self.student_id = f'STU{1000 + num:04d}'
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.student_id} — {self.first_name} {self.last_name}'

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
