from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import FeedBack,FeedBackCategory,FeedBackPriority,FeedBackStatus
from .serializers import FeedBackSerializer

# Create your views here.
class FeedBackViewSet(viewsets.ModelViewSet):
    queryset =  FeedBack.objects.all()
    serializer_class = FeedBackSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Allow filtering by various fileds"""
        queryset = FeedBack.objects.all()

        # filter by attendee id
        attendee_id = self.request.query_params.get('attended_id')
        if attendee_id:
            queryset = queryset.filter(attendee_id=attendee_id)

        # filter by category
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)

        # filter by priority
        priority = self.request.query_params.get('priority')
        if priority:
            queryset = queryset.filter(priority=priority)

        # filter by status
        status = self.request.query_params.get('status')
        if status:
            queryset = queryset.filter(status=status)

        # filter by minimum rating
        min_rating = self.request.query_params.get('min_rating')
        if min_rating:
            queryset = queryset.filter(rating__gte=min_rating)

        return queryset
    
    @action(detail=False,methods='get')
    def categories(self,request):
        """Return all available feedback in category"""
        return Response(dict(FeedBackCategory.choices))
    
    @action(detail=False,methods=['get'])
    def priorities(self,request):
        """Return all available priority levels"""
        return Response(dict(FeedBackPriority.choices))
    
    @action(detail=False,methods='get')
    def statuses(self,request):
        """Return all available status options"""
        return Response(dict(FeedBackStatus.choices))


