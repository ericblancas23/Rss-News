from rest_framework import serializers
from .models import Feed

class FeedSerializer(serializers.Model):
    class Meta:
        model = Feed
        fields = ('id', 'url')