from rest_framework import viewsets,status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Club
from .serializers import ClubSerializer
from django.shortcuts import get_object_or_404
from rest_framework import generics
# Create your views here.

class ClubViewSet(viewsets.ModelViewSet):
    queryset = Club.objects.prefetch_related('communities').all()
    serializer_class = ClubSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'put', 'patch']

    def list(self,request):
        clubs = self.get_queryset()
        serializer = self.get_serializer(clubs,many=True)
        return Response({
            'message':'Clubs retrieved successfully',
            'message':'success',
            'data':serializer.data
        },status=status.HTTP_200_OK)
    
    """I will comment out the view function to create a club because at this point we don't need it"""
    # def create(self,request):
    #     serializer = self.get_serializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response({
    #             'message':'Club created successfully',
    #             'status':'success',
    #             'data':serializer.data
    #         },status=status.HTTP_201_CREATED)
    
    def retrieve(self,request,pk=None):
        try:
            #club = self.get_object()
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            print("Serializer data:",serializer.data)
            print("Instance Data:", instance.__dict__)  
            return Response({
                'message':'Club retrieved successfully',
                'status':'succeess',
                'data':serializer.data
            },status =status.HTTP_200_OK)
        except Club.DoesNotExist:
            return Response({
                'message':'Club not found',
                'status':'error'
            },status=status.HTTP_404_NOT_FOUND)
    def update(self,request,pk=None):
        club = self.get_object()
        serializer = self.get_serializer(club, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message':'Club update successfully',
                'status':'success',
                'data':serializer.data
            },status=status.HTTP_200_OK)
        return Response({
            'message':'failed to update club',
            'status':'failed',
            'data':serializer.errors
        },status=status.HTTP_400_BAD_REQUEST)
    def destroy(self,request,pk=None):
        club = self.get_object()
        club.delete()
        return Response({
            'message':'Club deleted successfully',
            'status':'success',
            'data':[]
        },status=status.HTTP_200_OK)
    


    
# class ExecutiveMemberListCreateView(generics.ListCreateAPIView):
#     queryset = ExecutiveMember.objects.all()
#     serializer_class = ExecutiveMemberSerializer

# class ExecutiveMemberDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = ExecutiveMember.objects.all()
#     serializer_class = ExecutiveMemberSerializer

   


