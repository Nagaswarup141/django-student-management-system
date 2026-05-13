from rest_framework import generics, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Grade
from .serializers import GradeSerializer
from students.models import Student

class GradeListCreateView(generics.ListCreateAPIView):
    queryset           = Grade.objects.select_related('student','course')
    serializer_class   = GradeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends    = [filters.SearchFilter, filters.OrderingFilter]
    search_fields      = ['student__first_name','student__last_name','student__student_id']

    def get_queryset(self):
        qs         = super().get_queryset()
        student_id = self.request.query_params.get('student')
        course_id  = self.request.query_params.get('course')
        semester   = self.request.query_params.get('semester')
        if student_id: qs = qs.filter(student_id=student_id)
        if course_id:  qs = qs.filter(course_id=course_id)
        if semester:   qs = qs.filter(semester=semester)
        return qs

class GradeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset           = Grade.objects.all()
    serializer_class   = GradeSerializer
    permission_classes = [IsAuthenticated]

class ReportCardView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        sid      = request.query_params.get('student')
        semester = request.query_params.get('semester','')
        if not sid:
            return Response({'error':'student param required'}, status=400)
        student = Student.objects.get(id=sid)
        grades  = Grade.objects.filter(student=student)
        if semester: grades = grades.filter(semester=semester)
        total_credits = weighted_gp = 0
        grade_list = []
        for g in grades.select_related('course'):
            c = g.course.credits
            total_credits += c
            weighted_gp   += g.grade_points * c
            grade_list.append({'course':g.course.code,'course_name':g.course.name,'credits':c,
                'mid_term':float(g.mid_term),'final_exam':float(g.final_exam),'assignment':float(g.assignment),
                'total':g.total_marks,'percentage':g.percentage,'letter_grade':g.letter_grade,'grade_points':g.grade_points})
        gpa = round(weighted_gp/total_credits,2) if total_credits else 0
        return Response({'student':{'id':student.student_id,'name':student.full_name,'department':student.department,'year':student.year},
            'semester':semester,'grades':grade_list,'total_credits':total_credits,'gpa':gpa})

class LeaderboardView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        semester = request.query_params.get('semester','')
        result   = []
        for s in Student.objects.filter(is_active=True):
            grades = Grade.objects.filter(student=s)
            if semester: grades = grades.filter(semester=semester)
            if not grades.exists(): continue
            avg = sum(g.percentage for g in grades) / grades.count()
            result.append({'student_id':s.student_id,'name':s.full_name,'department':s.department,
                'avg_percentage':round(avg,2),'courses_count':grades.count()})
        result.sort(key=lambda x: x['avg_percentage'], reverse=True)
        return Response(result[:20])
