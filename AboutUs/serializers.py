from rest_framework import serializers
from .models import Club
from Innovation_WebApp.models import CommunityProfile
from Innovation_WebApp.serializers import CommunityProfileSerializer

class ClubSerializer(serializers.ModelSerializer):
    # communities = serializers.SerializerMethodField()
    # number_of_communities = serializers.SerializerMethodField()


    class Meta:
        model = Club
        fields = ['id', 'name', 'about_us', 'vision', 'mission', 'social_media']

    # def get_communities(self, obj):
    #     communities = obj.communities.all()
    #     # Make sure this is returning data
    #     print(f"Found {communities.count()} communities for club {obj.name}")
    #     return [{
    #         'id': comm.id,
    #         'name': comm.name,
    #         'community_lead': comm.community_lead,
    #         'total_members': comm.total_members
    #     } for comm in communities]
    
    # def get_number_of_communities(self, obj):
    #     return obj.communities.count()

    # def validate_social_media(self, value):
    #     if not isinstance(value, list):
    #         raise serializers.ValidationError("Social media must be a list")
        
    #     for item in value:
    #         if not isinstance(item, dict):
    #             raise serializers.ValidationError("Each social media item must be an object")
    #         if 'platform' not in item:
    #             raise serializers.ValidationError("Each social media item must have a platform")
    #         if 'url' not in item:
    #             raise serializers.ValidationError("Each social media item must have a URL")
        
#         return value
# class ExecutiveMemberSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ExecutiveMember
#         fields = ['id','name','position','bio','email',]


        

