from django.db import models


class Video(models.Model):
    video_id = models.CharField(max_length=16, unique=True, db_index=True)
    title = models.CharField(max_length=1024)
    description = models.TextField(blank=True, null=True)
    published_at = models.DateTimeField()
    thumbnail_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title