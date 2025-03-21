from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import FCMDevice
from .serializers import FCMDeviceSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register_device(request):
    serializer = FCMDeviceSerializer(data=request.data)
    if serializer.is_valid():
        # Check if token already exists for this user
        FCMDevice.objects.filter(
            user=request.user,
            device_token=serializer.validated_data['device_token']
        ).delete()

        # Create new device
        FCMDevice.objects.create(
            user=request.user,
            **serializer.validated_data
        )
        return Response({'success': True}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
