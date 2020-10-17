from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout, login
from django.contrib.auth.models import User
from django.contrib import messages
from img_storage.models import img_link_storage
from django.db.models import Max
from api_key import *
import tweepy

#twitter api
auth = tweepy.OAuthHandler(consumer_key, consumer_key_secret)
api = tweepy.API(auth)

# Create your views here.

def homepage_view(request, *args, **kwargs):

    if request.user.is_authenticated:
        context = {
            'handle': request.user.social_auth.get(provider='twitter').extra_data['access_token']['screen_name']
        }
        return render(request, "landingPage.html", context)
    else:
        return render(request, "landingPage.html", {})

def demo_view(request, *args, **kwargs):
    nssImgs_url = []
    tweets = api.user_timeline('1231405854194356224')
    for tweet in tweets:
        if tweet.source == "Nintendo Switch Share":
            for img_url in tweet.extended_entities['media']:
                if img_url['type'] == 'photo':
                    nssImgs_url.append(img_url['media_url'])
                else:
                    continue
    context = {
        'img_url': nssImgs_url
    }
    return render(request, "demo.html", context)

def gallery_view(request):
    if not request.user.is_authenticated:
        messages.add_message(request, messages.INFO, 'Login is required')
        return redirect('/', )
    
    db_user_objects = img_link_storage.objects.filter(media_owner=request.user).order_by('twitter_media_id')
    db_max_id = db_user_objects.aggregate(Max('tweet_id'))['tweet_id__max'] #find last entry in db

    #fetch existing img_url from db to img_list, reverse order so new images staies on top
    try:
        nssImgs_url = list(reversed(list(db_user_objects.values_list('media_url', flat=True))))
    #if no db entry exist, create an empty list to be processed
    except:
        nssImgs_url = []

    #api access tokens
    tokens = request.user.social_auth.get(provider='twitter').extra_data['access_token']
    auth.set_access_token(tokens['oauth_token'], tokens['oauth_token_secret'])
    tweets = api.user_timeline(tweet_mode="extended", since_id=db_max_id) #get tweets from twitter api

    for tweet in tweets:
        if tweet.source == "Nintendo Switch Share":
            for extended_entitie_media in tweet.extended_entities['media']:
                if extended_entitie_media['type'] == 'photo':
                    nssImgs_url.append(extended_entitie_media['media_url_https'])
                    db_entry = img_link_storage(media_owner=request.user, media_url=extended_entitie_media['media_url_https'], tweet_id=tweet.id, twitter_media_id=extended_entitie_media['id'])
                    db_entry.save()
                else:
                    continue
    
    context = {
        'img_url': nssImgs_url,
    }

    return render(request, "gallery.html", context)

def img_view_slug(request, twitter_media_id):
    return

def about_view(request):
    return render(request, "about.html", {})

def logout(request):
    auth_logout(request)
    return redirect('/')