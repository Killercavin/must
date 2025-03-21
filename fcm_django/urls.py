from django.urls import path
from . import views

urlpatterns = [
    path('users/register-device/', views.register_device, name='register_device'),
]