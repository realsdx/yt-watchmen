from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import pagination
from watchmen.serializers import VideoSerializer
from watchmen.models import Video

# remove this after adding cron job
from watchmen.utils import fetch_youtube_data

class VideoListPagination(pagination.PageNumberPagination):
    page_size = 10

class VideoList(viewsets.GenericViewSet, mixins.ListModelMixin):
    """ A Viewset for listing all the videos """

    serializer_class = VideoSerializer
    pagination_class = VideoListPagination
    queryset = Video.objects.all()
