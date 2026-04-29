from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError
from .serializers import EventPayloadSerializer
from .services.event_service import EventService
from .models import DailyUsageAggregate, Threshold

class EventIngestionView(APIView):
    def post(self, request):
        serializer = EventPayloadSerializer(data=request.data)
        if serializer.is_valid():
            try:
                EventService.process_event(serializer.validated_data)
                return Response({"status": "success"}, status=status.HTTP_201_CREATED)
            except (IntegrityError, ValidationError) as e:
                # Catch specific integrity or validation errors
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UsageDashboardView(APIView):
    def get(self, request):
        account_id = request.query_params.get('account_id')
        if not account_id:
            return Response({"error": "account_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Base query on the aggregated table
        qs = DailyUsageAggregate.objects.filter(account_id=account_id)

        # 1. Daily usage (overall usage grouped by date)
        daily_usage = qs.values('date').annotate(
            total=Sum('total_events')
        ).order_by('date')

        # 2. Feature usage (overall usage grouped by feature)
        feature_usage = qs.values('feature_name').annotate(
            total=Sum('total_events')
        ).order_by('-total')

        # 3. Team usage (overall usage grouped by team)
        team_usage = qs.values('team__name', 'team_id').annotate(
            total=Sum('total_events')
        ).order_by('-total')

        return Response({
            "daily_usage": list(daily_usage),
            "feature_usage": list(feature_usage),
            "team_usage": list(team_usage),
        })

class ThresholdView(APIView):
    def get(self, request):
        account_id = request.query_params.get('account_id')
        if not account_id:
            return Response({"error": "account_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        thresholds = Threshold.objects.filter(account_id=account_id).values('id', 'feature_name', 'limit')
        return Response(list(thresholds))

    def post(self, request):
        account_id = request.data.get('account_id')
        feature_name = request.data.get('feature_name')
        limit = request.data.get('limit')
        if not all([account_id, feature_name, limit]):
             return Response({"error": "Missing fields: account_id, feature_name, limit"}, status=status.HTTP_400_BAD_REQUEST)
        
        threshold, created = Threshold.objects.update_or_create(
            account_id=account_id, feature_name=feature_name, defaults={'limit': limit}
        )
        return Response({"status": "success", "id": threshold.id}, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
