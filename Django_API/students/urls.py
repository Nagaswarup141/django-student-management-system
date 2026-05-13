from django.urls import path
from .views import StudentListCreateView, StudentDetailView, StudentStatsView

urlpatterns = [
    path('',          StudentListCreateView.as_view(), name='student-list'),
    path('<int:pk>/', StudentDetailView.as_view(),     name='student-detail'),
    path('stats/',    StudentStatsView.as_view(),      name='student-stats'),
]
