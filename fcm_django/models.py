from django.db import models
from django .conf import settings

# Create your models here.

class FCMDevice(models.Model):
    #user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='fcm_devices')
    device_token = models.CharField(max_length=255,unique=True)
    platform = models.CharField(max_length=20) # "android" or "ios"
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s device ({self.platform})"
    
