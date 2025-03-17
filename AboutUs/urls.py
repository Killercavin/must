from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import ClubViewSet


router = DefaultRouter()
router.register(r'club',ClubViewSet)



urlpatterns = [
    path('', include(router.urls))
]
urlpatterns = [
    # path('executive-members/', ExecutiveMemberListCreateView.as_view(), name='executive-member-list'),
    # path('executive-members/<int:pk>/', ExecutiveMemberDetailView.as_view(), name='executive-member-detail'),
    # path('communities/', CommunityListCreateView.as_view(), name='community-list'),
    # path('communities/<int:pk>/', CommunityDetailView.as_view(), name='community-detail'),
]



