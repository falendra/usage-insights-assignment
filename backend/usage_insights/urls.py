from django.urls import path
from .views import EventIngestionView, UsageDashboardView, ThresholdView

urlpatterns = [
    path('events/', EventIngestionView.as_view(), name='event-ingestion'),
    path('usage/', UsageDashboardView.as_view(), name='usage-dashboard'),
    path('thresholds/', ThresholdView.as_view(), name='thresholds'),
]
