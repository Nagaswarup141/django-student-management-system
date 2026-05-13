"""fees/urls.py"""
from django.urls import path
from .views import FeeListCreateView, FeeDetailView, RecordPaymentView, FeeStatsView
urlpatterns = [
    path('',              FeeListCreateView.as_view(), name='fee-list'),
    path('<int:pk>/',     FeeDetailView.as_view(),     name='fee-detail'),
    path('<int:pk>/pay/', RecordPaymentView.as_view(),  name='fee-pay'),
    path('stats/',        FeeStatsView.as_view(),      name='fee-stats'),
]
