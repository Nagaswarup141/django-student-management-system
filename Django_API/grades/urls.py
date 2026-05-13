"""grades/urls.py"""
from django.urls import path
from .views import GradeListCreateView, GradeDetailView, ReportCardView, LeaderboardView
urlpatterns = [
    path('',             GradeListCreateView.as_view(), name='grade-list'),
    path('<int:pk>/',    GradeDetailView.as_view(),     name='grade-detail'),
    path('report-card/', ReportCardView.as_view(),      name='report-card'),
    path('leaderboard/', LeaderboardView.as_view(),     name='leaderboard'),
]
