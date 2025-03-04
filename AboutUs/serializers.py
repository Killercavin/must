from rest_framework import serializers
from .models import Club,ExecutiveMember,SocialMedia


class SocialMediaSerializer(serializers.ModelSerializer):
    platform = serializers.CharField()
    url = serializers.URLField()


class ExecutiveMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExecutiveMember
        fields = ['id','name','position','bio','email',]

# class CommunitySerializer(serializers.ModelSerializer):
#     executives = serializers.SerializerMethodField()
#     class Meta:
#         model = Community
#         fields = [
#             'id', 'name', 'community_lead', 'co_lead', 'secretary', 
#             'email', 'phone_number','social_media',
#             'description', 'founding_date', 'total_members', 
#             'is_recruiting', 'tech_stack', 'executives'
#         ]
        
#     def get_executives(self,obj):
#         executives = ExecutiveMember.objects.filter(Community=obj)
#         return ExecutiveMemberSerializer(executives,many=True).data
        
class ClubSerializers(serializers.ModelSerializer):
    social_media = SocialMediaSerializer(many=True,read_only=True)

    class Meta:
        model = Club
        fields = ['id', 'name', 'about_us', 'vision', 'mission', 'social_media']
        

    def get_communities(self,obj):
        communities = Community.objects.filter(club=obj)
        return CommunitySerializer(communities,many=True).data
    