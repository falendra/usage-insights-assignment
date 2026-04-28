from rest_framework import serializers

class EventPayloadSerializer(serializers.Serializer):
    account_id = serializers.IntegerField()
    user_id = serializers.IntegerField()
    team_id = serializers.IntegerField(required=False, allow_null=True)
    event_type = serializers.CharField(max_length=100)
    feature_name = serializers.CharField(max_length=100)
    metadata = serializers.JSONField(required=False, default=dict)
    timestamp = serializers.DateTimeField(required=False)
