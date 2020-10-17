from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class img_link_storage(models.Model):
    objects = None
    media_owner = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default='username_missing')
    media_url = models.URLField(unique=True)
    tweet_id = models.BigIntegerField()
    twitter_media_id = models.BigIntegerField(unique=True, primary_key=True)