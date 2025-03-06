from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta
import uuid

def get_default_expires_at():
    return timezone.now() + timedelta(hours=1)

# Create your models here.
class PasswordResetRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)
    old_password = models.CharField(max_length=128,null=True)
    new_password = models.CharField(max_length=128,null=True)
    expires_at = models.DateTimeField(default=get_default_expires_at)

    def is_expired(self):
        from django.utils import timezone
        return timezone.now() > self.expires_at

    def __str__(self):
        return f"Password change for {self.user.username} - {self.token}"
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #registration_no = models.CharField(max_length=50)
    course = models.CharField(max_length=50)


    def __str__(self):
        return self.user.username
