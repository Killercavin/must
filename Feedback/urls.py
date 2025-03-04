from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import FeedBackViewSet


router = DefaultRouter()
router.register(r'feedback',FeedBackViewSet)


urlpatterns = [
    path('feedback/',include(router.urls))
]