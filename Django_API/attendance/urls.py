"""attendance/urls.py"""
from django.urls import path
from .views import AttendanceListCreateView, AttendanceDetailView, BulkAttendanceView, AttendanceSummaryView
urlpatterns = [
    path('',         AttendanceListCreateView.as_view(), name='attendance-list'),
    path('<int:pk>/',AttendanceDetailView.as_view(),     name='attendance-detail'),
    path('bulk/',    BulkAttendanceView.as_view(),       name='attendance-bulk'),
    path('summary/', AttendanceSummaryView.as_view(),    name='attendance-summary'),
]
