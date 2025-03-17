from django.db import models

# Create your models here.
class Club(models.Model):
    name = models.CharField(max_length=200)
    about_us = models.TextField()
    vision = models.CharField(max_length=500)
    mission = models.CharField(max_length=500)
    social_media = models.JSONField(default=list, blank=True)
    
    def __str__(self):
        return self.name

class ExecutiveMember(models.Model):
    name = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    bio = models.TextField(blank=True, null=True)
    email = models.EmailField()

    def __str__(self):
        return f"{self.name} - {self.position}"
    
    