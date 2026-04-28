from django.urls import path
from .views import EventIngestionView, UsageDashboardView

urlpatterns = [
    path('events/', EventIngestionView.as_view(), name='event-ingestion'),
    path('usage/', UsageDashboardView.as_view(), name='usage-dashboard'),
]
