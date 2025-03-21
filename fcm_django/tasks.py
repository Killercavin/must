from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import Event
from .notifications import send_event_reminder

@shared_task
def schedule_event_reminders():
    """Schedule event reminders for upcoming events"""
    
    # Find events happening in 24 hours
    one_day_from_now = timezone.now() + timedelta(days=1)
    events_in_24h = Event.objects.filter(
        start_time__gte=one_day_from_now,
        start_time__lt=one_day_from_now + timedelta(minutes=30)
    )
    
    for event in events_in_24h:
        for participant in event.participants.all():
            send_event_reminder(
                event_id=event.id,
                user_id=participant.id,
                event_title=event.title,
                reminder_type="24h"
            )
    
    # Find events happening in 30 minutes
    thirty_mins_from_now = timezone.now() + timedelta(minutes=30)
    events_in_30min = Event.objects.filter(
        start_time__gte=thirty_mins_from_now,
        start_time__lt=thirty_mins_from_now + timedelta(minutes=5)
    )
    
    for event in events_in_30min:
        for participant in event.participants.all():
            send_event_reminder(
                event_id=event.id,
                user_id=participant.id,
                event_title=event.title,
                reminder_type="30min"
            )
    
    # Find recently completed events
    just_completed = timezone.now() - timedelta(minutes=10)
    completed_events = Event.objects.filter(
        end_time__gte=just_completed,
        end_time__lt=timezone.now()
    )
    
    for event in completed_events:
        for participant in event.participants.all():
            send_event_reminder(
                event_id=event.id,
                user_id=participant.id,
                event_title=event.title,
                reminder_type="completed"
            )
