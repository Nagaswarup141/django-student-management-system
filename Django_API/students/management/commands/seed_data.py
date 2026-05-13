from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from students.models import Student
from courses.models import Course
from grades.models import Grade
from fees.models import FeeRecord
from attendance.models import Attendance
import datetime, random

STUDENTS = [
    ('Arjun','Sharma','CS',2,'arjun@uni.edu','+91 98765 43210','Male'),
    ('Priya','Patel','CS',3,'priya@uni.edu','+91 87654 32109','Female'),
    ('Rahul','Verma','EE',1,'rahul@uni.edu','+91 76543 21098','Male'),
    ('Sneha','Reddy','BBA',2,'sneha@uni.edu','+91 65432 10987','Female'),
    ('Karan','Singh','ME',4,'karan@uni.edu','+91 54321 09876','Male'),
    ('Ananya','Gupta','CS',1,'ananya@uni.edu','+91 43210 98765','Female'),
    ('Vikram','Nair','EE',3,'vikram@uni.edu','+91 32109 87654','Male'),
    ('Divya','Menon','CS',2,'divya@uni.edu','+91 21098 76543','Female'),
    ('Amit','Joshi','ME',1,'amit@uni.edu','+91 10987 65432','Male'),
    ('Kavya','Rao','BBA',3,'kavya@uni.edu','+91 99887 76655','Female'),
]

COURSES = [
    ('CS101','Algorithms','CS',4,'Dr. Priya Sharma','Fall 2024'),
    ('CS201','Database Mgmt Systems','CS',4,'Prof. Rajan Mehta','Fall 2024'),
    ('CS301','AI & Machine Learning','CS',3,'Dr. Anil Kumar','Fall 2024'),
    ('EE101','Electric Circuits','EE',4,'Dr. Sita Nair','Fall 2024'),
    ('MA101','Engineering Calculus','ME',3,'Prof. Vikram Das','Fall 2024'),
    ('BBA101','Business Analytics','BBA',3,'Dr. Meena Joshi','Fall 2024'),
]

class Command(BaseCommand):
    help = 'Seed demo data for StudentMS'

    def handle(self, *args, **kwargs):
        self.stdout.write('🌱 Seeding database...')

        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin','admin@edutrack.com','admin123')
            self.stdout.write(self.style.SUCCESS('  ✓ Admin: admin / admin123'))

        courses = []
        for code,name,dept,credits,instructor,semester in COURSES:
            c,_ = Course.objects.get_or_create(code=code, defaults=dict(
                name=name,department=dept,credits=credits,instructor=instructor,semester=semester))
            courses.append(c)
        self.stdout.write(self.style.SUCCESS(f'  ✓ {len(courses)} courses'))

        students = []
        for fname,lname,dept,year,email,phone,gender in STUDENTS:
            s,_ = Student.objects.get_or_create(email=email, defaults=dict(
                first_name=fname,last_name=lname,department=dept,year=year,
                phone=phone,gender=gender,address='Hyderabad, Telangana'))
            students.append(s)
        self.stdout.write(self.style.SUCCESS(f'  ✓ {len(students)} students'))

        for s in students:
            for c in courses[:3]:
                Grade.objects.get_or_create(student=s,course=c,semester='Fall 2024',
                    defaults=dict(mid_term=random.randint(22,38),final_exam=random.randint(32,57),assignment=random.randint(11,19)))
        self.stdout.write(self.style.SUCCESS('  ✓ Grades seeded'))

        for i,s in enumerate(students):
            paid = 45000 if i<7 else 22500 if i<9 else 0
            FeeRecord.objects.get_or_create(student=s,course=courses[0],semester='Fall 2024',
                defaults=dict(total_amount=45000,paid_amount=paid,due_date=datetime.date(2025,3,31),payment_mode='Online'))
        self.stdout.write(self.style.SUCCESS('  ✓ Fees seeded'))

        today = datetime.date.today()
        statuses = ['Present','Present','Present','Absent','Late','Present','Present','Present']
        for s in students[:5]:
            for offset in range(20):
                date = today - datetime.timedelta(days=offset)
                if date.weekday() >= 5: continue
                Attendance.objects.get_or_create(student=s,course=courses[0],date=date,
                    defaults={'status': statuses[offset % len(statuses)]})
        self.stdout.write(self.style.SUCCESS('  ✓ Attendance seeded'))

        self.stdout.write(self.style.SUCCESS('\n✅ Done! Login: admin / admin123'))
        self.stdout.write('   Admin: http://127.0.0.1:8000/admin/')
