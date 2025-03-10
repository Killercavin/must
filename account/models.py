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
    


# forgot password
class OTP(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_verified = models.BooleanField(default=False)

    def save(self,*args,**Kwargs):
        if not self.expires_at:
            # Set expiration time to 10 minutes from creation
            self.expires_at = timezone.now() + timedelta(minutes=10)
        super().save(*args,**Kwargs)
    
    def is_valid(self):
        return not self.is_verified and timezone.now() <= self.expires_at
    

class PasswordResetSession(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    otp = models.ForeignKey(OTP,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    def save(self,*args,**kwargs):
        if not self.expires_at:
            # Set expiration time to 10 minutes from creation
            self.expires_at = timezone.now() + timedelta(minutes=10)
        super().save(*args, **kwargs)


    def is_valid(self):
        return not self.is_used and timezone.now() <= self.expires_at
