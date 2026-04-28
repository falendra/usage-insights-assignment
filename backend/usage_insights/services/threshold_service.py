import logging
from django.db.models import Sum
from usage_insights.models import Threshold, DailyUsageAggregate

logger = logging.getLogger(__name__)

class ThresholdService:
    @staticmethod
    def check_thresholds(event):
        try:
            threshold = Threshold.objects.get(
                account_id=event.account_id,
                feature_name=event.feature_name
            )
        except Threshold.DoesNotExist:
            return

        # Calculate the total usage for this account and feature
        # (Summing across all teams and dates for simplicity, or we could scope by date)
        usage = DailyUsageAggregate.objects.filter(
            account_id=event.account_id,
            feature_name=event.feature_name
        ).aggregate(total=Sum('total_events'))['total'] or 0

        if usage > threshold.limit:
            # Log the exact message requested
            logger.info(f"Threshold exceeded for account {event.account_id}")
