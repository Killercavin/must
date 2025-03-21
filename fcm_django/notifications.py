import time
from firebase_admin import messaging
from .models import FCMDevice


def send_notification_to_user(user_id, title, body, data=None):
    """Send notification to all devices of a specific user"""
    if data is None:
        data = {}
    
    # Get all active devices for this user
    devices = FCMDevice.objects.filter(user_id=user_id, active=True)
    
    for device in devices:
        message = messaging.Message(
            token=device.device_token,
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            data=data,
            android=messaging.AndroidConfig(
                priority='high',
            ),
        )
        try:
            response = messaging.send(message)
            print(f"Successfully sent message: {response}")
        except Exception as e:
            print(f"Error sending message to {device.device_token}: {e}")

def send_event_reminder(event_id, user_id, event_title, reminder_type):
    """Send event reminder notification"""
    
    # Determine message based on reminder type
    if reminder_type == "24h":
        title = "Event Reminder"
        body = f"{event_title} is happening in 24 hours"
    elif reminder_type == "30min":
        title = "Event Starting Soon"
        body = f"{event_title} is starting in 30 minutes"
    elif reminder_type == "completed":
        title = "Event Completed"
        body = f"{event_title} has finished. We hope you enjoyed it!"
    else:
        title = "Event Update"
        body = f"Update for your event: {event_title}"
    
    # Prepare data payload
    data = {
        "type": "event_reminder",
        "eventId": str(event_id),
        "title": title,
        "message": body,
        "timestamp": str(int(time.time() * 1000))
    }
    
    # Send notification
    send_notification_to_user(user_id, title, body, data)