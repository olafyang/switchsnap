from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from django.contrib import messages
from img_storage.models import img_link_storage
from django.db.models import Max
from api_key import *
import tweepy

# twitter api
auth = tweepy.OAuthHandler(consumer_key, consumer_key_secret)
api = tweepy.API(auth)


# Create your views here.

def homepage_view(request):
    if request.user.is_authenticated:
        context = {
            'handle': request.user.social_auth.get(provider='twitter').extra_data['access_token']['screen_name']
        }
        return render(request, "home.html", context)
    else:
        return render(request, "home.html", {})


def demo_view(request):
    db_user_objects = img_link_storage.objects.filter(media_owner=User.objects.get(username='olafyxyz')).order_by(
        'twitter_media_id')
    db_max_id = db_user_objects.aggregate(Max('tweet_id'))['tweet_id__max']  # find last entry in db
    nss_images = db_user_objects.reverse()

    # get tweets from twitter api
    tweets = api.user_timeline(id='1231405854194356224', tweet_mode="extended", since_id=db_max_id)
    for tweet in tweets:
        if tweet.source == "Nintendo Switch Share":
            for extended_entity_media in tweet.extended_entities['media']:
                if extended_entity_media['type'] == 'photo':
                    nss_images[tweet.id] = extended_entity_media['media_url_https']
                else:
                    continue
    context = {
        'img_dict': nss_images
    }
    return render(request, "demo.html", context)


def gallery_view(request, number_of_result=10):
    # check if user is logged in
    if not request.user.is_authenticated:  # not working
        messages.add_message(request, messages.INFO, 'Login is required')
        return redirect('/')

    # fetch user media entry form db
    db_user_objects = img_link_storage.objects.filter(media_owner=request.user).order_by('twitter_media_id')
    db_max_id = db_user_objects.aggregate(Max('tweet_id'))['tweet_id__max']  # find last entry in db
    nss_images = db_user_objects.reverse()[:number_of_result]

    # api access tokens
    tokens = request.user.social_auth.get(provider='twitter').extra_data['access_token']
    auth.set_access_token(tokens['oauth_token'], tokens['oauth_token_secret'])
    tweets = api.user_timeline(tweet_mode="extended", since_id=db_max_id)  # get tweets from twitter api

    for tweet in tweets:
        if tweet.source == "Nintendo Switch Share":
            for extended_entity_media in tweet.extended_entities['media']:
                if extended_entity_media['type'] == 'photo':
                    nss_images[tweet.id] = extended_entity_media['media_url_https']
                    db_entry = img_link_storage(media_owner=request.user,
                                                media_url=extended_entity_media['media_url_https'], tweet_id=tweet.id,
                                                twitter_media_id=extended_entity_media['id'])
                    db_entry.save()
                else:
                    continue

    context = {
        'img_dict': nss_images,
        'n': number_of_result,
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
