import pytest
import logging
from rest_framework.test import APIClient
from usage_insights.models import Account, Team, User, Event, DailyUsageAggregate, Threshold

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def setup_data():
    account = Account.objects.create(name="Test Account")
    team = Team.objects.create(account=account, name="Test Team")
    user = User.objects.create(account=account, team=team, email="test@example.com", name="Test User")
    Threshold.objects.create(account=account, feature_name="dashboard", limit=5)
    return {
        "account": account,
        "team": team,
        "user": user
    }

@pytest.mark.django_db
def test_event_ingestion(api_client, setup_data):
    payload = {
        "account_id": setup_data["account"].id,
        "user_id": setup_data["user"].id,
        "team_id": setup_data["team"].id,
        "event_type": "click",
        "feature_name": "dashboard",
        "metadata": {"button": "save"}
    }
    
    response = api_client.post('/api/events/', payload, format='json')
    assert response.status_code == 201
    assert response.json()["status"] == "success"
    
    # Verify raw event created
    assert Event.objects.count() == 1
    event = Event.objects.first()
    assert event.event_type == "click"

@pytest.mark.django_db
def test_aggregation(api_client, setup_data):
    payload = {
        "account_id": setup_data["account"].id,
        "user_id": setup_data["user"].id,
        "team_id": setup_data["team"].id,
        "event_type": "view",
        "feature_name": "reports"
    }
    
    # Send 3 events
    for _ in range(3):
        api_client.post('/api/events/', payload, format='json')
        
    # Verify aggregation
    assert DailyUsageAggregate.objects.count() == 1
    agg = DailyUsageAggregate.objects.first()
    assert agg.total_events == 3
    assert agg.feature_name == "reports"

@pytest.mark.django_db
def test_threshold_logic(api_client, setup_data, caplog):
    payload = {
        "account_id": setup_data["account"].id,
        "user_id": setup_data["user"].id,
        "team_id": setup_data["team"].id,
        "event_type": "click",
        "feature_name": "dashboard"
    }
    
    # Limit is 5. Let's send 6 events.
    with caplog.at_level(logging.INFO):
        for _ in range(6):
            api_client.post('/api/events/', payload, format='json')
            
    # Check if threshold exceeded message was logged
    assert f"Threshold exceeded for account {setup_data['account'].id}" in caplog.text
