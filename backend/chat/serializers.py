from rest_framework import serializers
from .models import Message, Channel

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["chat_name", "username", "message"]

class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = "__all__"