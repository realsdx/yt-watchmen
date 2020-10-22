from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from watchmen.serializers import VideoSerializer
from watchmen.models import Video

# remove this after adding cron job
from watchmen.utils import fetch_youtube_data

class VideoViewSet(viewsets.ViewSet):
    """ A Viewset for listing all the videos """
    fetch_youtube_data()

    def list(self, request):
        queryset = Video.objects.all()
        serializers = VideoSerializer(queryset, many=True)
        return Response(serializers.data)

