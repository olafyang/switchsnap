from django.db import models
from django.contrib.auth.models import User
from django.utils.dateparse import parse_duration


# Create your models here.
class img_link_storage(models.Model):
    objects = None
    media_owner = models.ForeignKey(User, on_delete=models.CASCADE)
    media_url = models.URLField(unique=True)
    tweet_id = models.BigIntegerField()
    media_type = models.CharField(max_length=5)
    vid_length = models.DurationField(null=True, blank=True)
    twitter_media_id = models.BigIntegerField(unique=True, primary_key=True)

    def duration_in_seconds(self):
        duration = self.vid_length.total_seconds()

        min = duration // 60
        min = int(min % 60)
        sec = int(duration % 60)

        return '{:02d}:{:02d}'.format(min, sec)
