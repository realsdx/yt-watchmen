from rest_framework import serializers
from watchmen.models import Video


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['title', 'description', 'published_at', 'thumbnail_url']
