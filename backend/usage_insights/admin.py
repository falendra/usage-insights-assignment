from django.contrib import admin
from .models import Account, Team, User, Event, DailyUsageAggregate, Threshold

admin.site.register(Account)
admin.site.register(Team)
admin.site.register(User)
admin.site.register(Event)
admin.site.register(DailyUsageAggregate)
admin.site.register(Threshold)
