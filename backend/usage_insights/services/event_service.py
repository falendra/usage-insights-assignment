from usage_insights.models import Event
from .aggregation_service import AggregationService
from .threshold_service import ThresholdService

class EventService:
    @staticmethod
    def process_event(validated_data):
        # Extract timestamp as it requires a separate save to override auto_now_add
        timestamp = validated_data.pop('timestamp', None)
        
        # Create Raw Event
        event = Event.objects.create(**validated_data)
        
        # If timestamp was explicitly provided in the payload, override it
        if timestamp:
            event.timestamp = timestamp
            event.save(update_fields=['timestamp'])
        
        # 1. Aggregate the event data
        AggregationService.aggregate_event(event)
        
        # 2. Check and notify if thresholds are exceeded
        ThresholdService.check_thresholds(event)
        
        return event
