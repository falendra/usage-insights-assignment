from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum
from .serializers import EventPayloadSerializer
from .services.event_service import EventService
from .models import DailyUsageAggregate

class EventIngestionView(APIView):
    def post(self, request):
        serializer = EventPayloadSerializer(data=request.data)
        if serializer.is_valid():
            try:
                EventService.process_event(serializer.validated_data)
                return Response({"status": "success"}, status=status.HTTP_201_CREATED)
            except Exception as e:
                # Catch integrity errors like foreign key constraints
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
