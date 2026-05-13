from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Attendance
from .serializers import AttendanceSerializer

class AttendanceListCreateView(generics.ListCreateAPIView):
    queryset           = Attendance.objects.select_related('student','course')
    serializer_class   = AttendanceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs         = super().get_queryset()
        student_id = self.request.query_params.get('student')
        course_id  = self.request.query_params.get('course')
        date       = self.request.query_params.get('date')
        month      = self.request.query_params.get('month')
        if student_id: qs = qs.filter(student_id=student_id)
        if course_id:  qs = qs.filter(course_id=course_id)
        if date:       qs = qs.filter(date=date)
        if month:      qs = qs.filter(date__month=month)
        return qs

    def perform_create(self, serializer):
        serializer.save(marked_by=self.request.user)

class AttendanceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset           = Attendance.objects.all()
    serializer_class   = AttendanceSerializer
    permission_classes = [IsAuthenticated]

class BulkAttendanceView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        from courses.models import Course
        course  = Course.objects.get(id=request.data.get('course'))
        date    = request.data.get('date')
        records = request.data.get('records', [])
        created = updated = 0
        for rec in records:
            obj, is_new = Attendance.objects.update_or_create(
                student_id=rec['student'], course=course, date=date,
                defaults={'status': rec.get('status','Present'), 'marked_by': request.user}
            )
            if is_new: created += 1
            else:      updated += 1
        return Response({'created': created, 'updated': updated})

class AttendanceSummaryView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        sid = request.query_params.get('student')
        if not sid:
            return Response({'error': 'student param required'}, status=400)
        records = Attendance.objects.filter(student_id=sid)
        total   = records.count()
        present = records.filter(status='Present').count()
        pct     = round((present/total*100),1) if total else 0
        return Response({'total': total, 'present': present, 'percentage': pct})
