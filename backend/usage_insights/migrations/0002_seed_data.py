from django.db import migrations

def seed_data(apps, schema_editor):
    Account = apps.get_model('usage_insights', 'Account')
    Team = apps.get_model('usage_insights', 'Team')
    User = apps.get_model('usage_insights', 'User')
    Threshold = apps.get_model('usage_insights', 'Threshold')

    # Create dummy account
    account, _ = Account.objects.get_or_create(id=1, defaults={'name': 'Demo Account'})

    # Create dummy team
    team, _ = Team.objects.get_or_create(id=1, defaults={'account': account, 'name': 'Engineering'})

    # Create dummy user
    User.objects.get_or_create(id=1, defaults={'account': account, 'team': team, 'email': 'user@demo.com', 'name': 'Demo User'})

    # Create a threshold so the user can test the logger
    Threshold.objects.get_or_create(account=account, feature_name='dashboard', defaults={'limit': 5})

def reverse_seed_data(apps, schema_editor):
    Account = apps.get_model('usage_insights', 'Account')
    Account.objects.filter(id=1).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('usage_insights', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_data, reverse_seed_data),
    ]
