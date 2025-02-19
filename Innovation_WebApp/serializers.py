from grpc import Status
from requests import Response, Session
from rest_framework import serializers

from Innovation_WebApp.Email import send_ticket_email
from .models import CommunityMember, SubscribedUsers, Events,EventRegistration,CommunityProfile,CommunitySession,Testimonial
import boto3
from django.conf import settings
import uuid



from .utils import send_ticket_email
import logging

logger = logging.getLogger(__name__)

class SubscribedUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscribedUsers
        fields = ['id', 'email', 'created_date']


class EventsSerializer(serializers.ModelSerializer):
    image_field = serializers.ImageField(write_only=True, required=False)  # To handle image upload
    image_url = serializers.URLField(read_only=True)  # To return the S3 URL

    class Meta:
        model = Events
        fields = '__all__'
        extra_kwargs = {
            'image_url': {'read_only': True}  # This field will store the S3 URL and is read-only
        }

    def create(self, validated_data):
        image_file = validated_data.pop('image_field', None)
        print("Starting creating process....")
        print(f"Image file is in validated_data: {image_file}")
        
        event_instance = Events.objects.create(**validated_data)
        print(f"Event instance created with ID: {event_instance.id}")

        if image_file:
            try:
                s3_client = boto3.client(
                    's3',
                    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                )

                filename = f"event_images/{uuid.uuid4()}_{image_file.name}"
                print(f"Generated filename: {filename}")

                image_file.seek(0)
                s3_client.upload_fileobj(
                    image_file,
                    settings.AWS_STORAGE_BUCKET_NAME,
                    filename,
                    ExtraArgs={'ContentType': image_file.content_type}
                )
                print("S3 upload completed")

                s3_url = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{filename}"
                print(f"Setting S3 URL: {s3_url}")
                # Here we update image_url instead of image
                event_instance.image_url = s3_url
                event_instance.save()

            except Exception as e:
                print(f"Error uploading to S3: {str(e)}")
                import traceback
                print(f"Traceback: {traceback.format_exc()}")
                raise serializers.ValidationError(f"Failed to upload image to S3: {str(e)}")

        return event_instance

    def update(self, instance, validated_data):
        image_file = validated_data.pop('image_field', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if image_file:
            s3_client = boto3.client(
                's3',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
            )

            filename = f"event_images/{uuid.uuid4()}_{image_file.name}"
            s3_client.upload_fileobj(
                image_file,
                settings.AWS_STORAGE_BUCKET_NAME,
                filename,
                ExtraArgs={'ContentType': image_file.content_type}
            )

            s3_url = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{filename}"
            # Here we update image_url instead of image
            instance.image_url = s3_url

        instance.save()
        return instance

class EventRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventRegistration
        fields = '__all__'
        #exclude = ('uid',)
        read_only_fields = [ 'registration_timestamp', 'ticket_number']

    def create(self, validated_data):
        registration = super().create(validated_data)
        
        # Send ticket email
        send_ticket_email(registration)
        
        return registration
    
class CommunitySessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunitySession
        fields = ['day', 'start_time', 'end_time', 'meeting_type', 'location']

class CommunityMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityMember
        fields = ['id', 'name', 'email', 'joined_at']

class CommunityProfileSerializer(serializers.ModelSerializer):
    sessions = CommunitySessionSerializer(many=True, read_only=True)
    members = CommunityMemberSerializer(many=True, read_only=True)
    
    class Meta:
        model = CommunityProfile
        fields = [
            'id', 'name', 'community_lead', 'co_lead', 
            'secretary', 'email', 'phone_number', 
            'github_link', 'linkedin_link', 'description', 
            'founding_date',  'is_recruiting', 
            'tech_stack','members','total_members','sessions'
        ]

    def create(self, validated_data):
        sessions_data = validated_data.pop('sessions', [])
        members_data = validated_data.pop('members', []) 
        community = CommunityProfile.objects.create(**validated_data)
        
        # Create sessions
        for session_data in sessions_data:
            Session.objects.create(community=community, **session_data)
        
        #Create members
        for member_data in members_data:
            CommunityMember.objects.create(community=community, **member_data)
        
        #Update total members
        community.update_total_members()
        
        return community

    def update(self, instance, validated_data):
        sessions_data = validated_data.pop('sessions', [])
        members_data = validated_data.pop('members', [])
        
        # Update community profile attributes
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update sessions
        instance.sessions.all().delete()
        for session_data in sessions_data:
            Session.objects.create(community=instance, **session_data)
        
        # Update members
        instance.members.all().delete()
        for member_data in members_data:
            CommunityMember.objects.create(community=instance, **member_data)
        
        # Update total members
        instance.update_total_members()
        
        return instance

class TestimonialSerializer(serializers.ModelSerializer):
    #author_username = serializers.ReadOnlyField(source='author.username')
    
    class Meta:
        model = Testimonial
        # fields = [
        #     'id', 'author_username', 'community', 
        #     'content', 'rating', 'created_at'
        # ]
        # read_only_fields = ['author', 'created_at']

# class CommunityCategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CommunityCategory
#         fields = ['id', 'name', 'description']




class CommunityJoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityMember
        fields = ['community', 'name', 'email']