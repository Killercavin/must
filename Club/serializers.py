
from rest_framework import serializers
from .models import Club, ExecutiveMember

class ClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = '__all__'

class ExecutiveMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExecutiveMember
        fields = '__all__'
from rest_framework import serializers
from .models import Club, ExecutiveMember

class ClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = '__all__'

class ExecutiveMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExecutiveMember
        fields = '__all__'