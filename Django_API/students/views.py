from rest_framework import generics, filters, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Student
from .serializers import StudentSerializer, StudentListSerializer


class StudentListCreateView(generics.ListCreateAPIView):
    queryset           = Student.objects.filter(is_active=True)
    permission_classes = [IsAuthenticated]
    filter_backends    = [filters.SearchFilter, filters.OrderingFilter]
    search_fields      = ['first_name','last_name','email','student_id']
    ordering_fields    = ['created_at','first_name','last_name','year']
    ordering           = ['-created_at']

    def get_serializer_class(self):
        return StudentListSerializer if self.request.method == 'GET' else StudentSerializer

    def get_queryset(self):
        qs   = super().get_queryset()
        dept = self.request.query_params.get('department')
        year = self.request.query_params.get('year')
        if dept: qs = qs.filter(department=dept)
        if year: qs = qs.filter(year=year)
        return qs


class StudentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset           = Student.objects.all()
    serializer_class   = StudentSerializer
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        student = self.get_object()
        student.is_active = False
        student.save()
        return Response({'message': 'Student deactivated.'}, status=status.HTTP_200_OK)


class StudentStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        total   = Student.objects.filter(is_active=True).count()
        by_dept = {}
        for dept, _ in Student.department.field.choices:
            by_dept[dept] = Student.objects.filter(department=dept, is_active=True).count()
        return Response({'total_students': total, 'by_department': by_dept})
