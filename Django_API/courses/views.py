from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from .models import Course
from .serializers import CourseSerializer

class CourseListCreateView(generics.ListCreateAPIView):
    queryset           = Course.objects.filter(is_active=True)
    serializer_class   = CourseSerializer
    permission_classes = [IsAuthenticated]
    filter_backends    = [filters.SearchFilter, filters.OrderingFilter]
    search_fields      = ['code','name','instructor']

    def get_queryset(self):
        qs   = super().get_queryset()
        dept = self.request.query_params.get('department')
        if dept: qs = qs.filter(department=dept)
        return qs

class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset           = Course.objects.all()
    serializer_class   = CourseSerializer
    permission_classes = [IsAuthenticated]
