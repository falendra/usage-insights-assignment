from usage_insights.models import Event
from .aggregation_service import AggregationService

class EventService:
    @staticmethod
    def process_event(validated_data):
        # Create Raw Event
        event_kwargs = {
            'account_id': validated_data['account_id'],
            'user_id': validated_data['user_id'],
            'event_type': validated_data['event_type'],
            'feature_name': validated_data['feature_name'],
        }
        if 'team_id' in validated_data and validated_data['team_id'] is not None:
            event_kwargs['team_id'] = validated_data['team_id']
        if 'metadata' in validated_data:
            event_kwargs['metadata'] = validated_data['metadata']

        event = Event.objects.create(**event_kwargs)
        
        # Note: If timestamp is provided in the payload, we update it.
        # Otherwise, the model's auto_now_add will set it to current time.
        if 'timestamp' in validated_data:
            event.timestamp = validated_data['timestamp']
            event.save()
        
        # Call aggregation
        AggregationService.aggregate_event(event)
        
        # Threshold logic here later
        return event
