from usage_insights.models import Event
from .aggregation_service import AggregationService
from .threshold_service import ThresholdService

class EventService:
    @staticmethod
    def process_event(validated_data):
        # Create Raw Event directly. Timestamp uses timezone.now default if not provided
        event = Event.objects.create(**validated_data)
        
        # 1. Aggregate the event data
        AggregationService.aggregate_event(event)
        
        # 2. Check and notify if thresholds are exceeded
        ThresholdService.check_thresholds(event)
        
        return event
