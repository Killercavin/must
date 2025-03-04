from rest_framework import serializers
from .models import FeedBack

class FeedBackSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedBack
        fields = '__all__'
        read_only_fields = ['id','submitted_at','updated_at']

        