from django.db.models import F
from usage_insights.models import DailyUsageAggregate

class AggregationService:
    @staticmethod
    def aggregate_event(event):
        event_date = event.timestamp.date()
        
        # We update the most granular aggregate record (by account, team, feature, date).
        # This single record implicitly tracks daily usage, feature usage, and team usage
        # since we can group by any of these dimensions when querying the dashboard.
        aggregate, created = DailyUsageAggregate.objects.get_or_create(
            account_id=event.account_id,
            team_id=event.team_id,
            feature_name=event.feature_name,
            date=event_date,
            defaults={'total_events': 0}
        )
        
        # Use F() expression to ensure atomicity and prevent race conditions when incrementing
        aggregate.total_events = F('total_events') + 1
        aggregate.save(update_fields=['total_events'])

