from django.db import models

class Account(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Team(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='teams')
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.account.name})"

class User(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='users')
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name='users')
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

class Event(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='events')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='events')
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name='events')
    event_type = models.CharField(max_length=100)
    feature_name = models.CharField(max_length=100)
    metadata = models.JSONField(default=dict, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['account', 'feature_name', 'timestamp']),
        ]

    def __str__(self):
        return f"{self.event_type} - {self.feature_name}"

class DailyUsageAggregate(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='daily_aggregates')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True, related_name='daily_aggregates')
    feature_name = models.CharField(max_length=100)
    date = models.DateField()
    total_events = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('account', 'team', 'feature_name', 'date')

    def __str__(self):
        return f"{self.account.name} - {self.feature_name} - {self.date}: {self.total_events}"

class Threshold(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='thresholds')
    feature_name = models.CharField(max_length=100)
    limit = models.PositiveIntegerField()

    class Meta:
        unique_together = ('account', 'feature_name')

    def __str__(self):
        return f"{self.account.name} - {self.feature_name} Limit: {self.limit}"
