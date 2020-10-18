from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout, login
from django.contrib.auth.models import User
from django.contrib import messages
from img_storage.models import img_link_storage
from django.db.models import Max
from api_key import *
import tweepy

0  # twitter api
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
    m_owner = User.objects.get(username='olafyxyz')
    db_user_objects = img_link_storage.objects.filter(media_owner=m_owner).order_by('twitter_media_id')
    db_max_id = db_user_objects.aggregate(Max('tweet_id'))['tweet_id__max']  # find last entry in db
    nssImgs = dict(zip(list(reversed(list(db_user_objects.values_list('twitter_media_id', flat=True)))),
                       list(reversed(list(db_user_objects.values_list('media_url', flat=True))))))

    # get tweets from twitter api
    tweets = api.user_timeline(id='1231405854194356224', tweet_mode="extended", since_id=db_max_id)
    for tweet in tweets:
        if tweet.source == "Nintendo Switch Share":
            for extended_entity_media in tweet.extended_entities['media']:
                if extended_entity_media['type'] == 'photo':
                    nssImgs[tweet.id] = extended_entity_media['media_url_https']
                else:
                    continue
    context = {
        'img_dict': nssImgs
    }
    return render(request, "demo.html", context)


def gallery_view(request):
    # check if user is logged in
    if not request.user.is_authenticated:
        messages.add_message(request, messages.INFO, 'Login is required')
        return redirect('/', )

    db_user_objects = img_link_storage.objects.filter(media_owner=request.user).order_by('twitter_media_id')
    db_max_id = db_user_objects.aggregate(Max('tweet_id'))['tweet_id__max']  # find last entry in db

    # fetch existing img_url from db to img_list, reverse order so new images staies on top
    try:
        nssImgs = dict(zip(list(reversed(list(db_user_objects.values_list('twitter_media_id', flat=True)))),
                           list(reversed(list(db_user_objects.values_list('media_url', flat=True))))))
    # if no db entry exist, create an empty list to be processed
    except:
        nssImgs = {}

    # api access tokens
    tokens = request.user.social_auth.get(provider='twitter').extra_data['access_token']
    auth.set_access_token(tokens['oauth_token'], tokens['oauth_token_secret'])
    tweets = api.user_timeline(tweet_mode="extended", since_id=db_max_id)  # get tweets from twitter api

    for tweet in tweets:
        if tweet.source == "Nintendo Switch Share":
            for extended_entity_media in tweet.extended_entities['media']:
                if extended_entity_media['type'] == 'photo':
                    # nssImgs_url.append(extended_entitiy_media['media_url_https'])
                    # nssImgs_tweet_id.append(tweet.id)
                    nssImgs[tweet.id] = extended_entity_media['media_url_https']
                    db_entry = img_link_storage(media_owner=request.user,
                                                media_url=extended_entity_media['media_url_https'], tweet_id=tweet.id,
                                                twitter_media_id=extended_entity_media['id'])
                    db_entry.save()
                else:
                    continue

    context = {
        'img_dict': nssImgs
    }

    return render(request, "gallery.html", context)


def img_view(request, media_id):
    db_img_obj = img_link_storage.objects.get(twitter_media_id=media_id)
    context = {
        'img_link': db_img_obj.media_url,
        'tweet_id': db_img_obj.tweet_id,
    }
    return render(request, 'imgview.html', context)


def about_view(request):
    return render(request, "about.html", {})


def logout(request):
    auth_logout(request)
    return redirect('/')
