from django.urls import path, include
from rest_framework import routers
from watchmen import views


router = routers.DefaultRouter()
router.register(r'videos', views.VideoList, basename='video')

urlpatterns = [
    path('', include(router.urls)),
]