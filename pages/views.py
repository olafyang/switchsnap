from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from img_storage.models import img_link_storage
from django.db.models import Max
from api_key import *
import tweepy
from datetime import timedelta


# custom methods
def get_largest_video(extended_entity_media):
    vid_variants = {}
    for vid in extended_entity_media['video_info']['variants']:
        if not vid['content_type'] == 'video/mp4':
            continue
        else:
            vid_variants[vid['bitrate']] = vid['url']
    return vid_variants[max(vid_variants.keys())]


# twitter api
auth = tweepy.OAuthHandler(consumer_key, consumer_key_secret)
tw_api = tweepy.API(auth)


# Create your views here.

def homepage_view(request):
    try:
        handle = '@' + request.user.social_auth.get(provider='twitter').extra_data['access_token']['screen_name']
    except:
        handle = ''
    context = {
        'handle': handle
    }
    return render(request, "home.html", context)


def demo_view(request, number_of_result=50):
    db_user_objects = img_link_storage.objects.filter(media_owner=User.objects.get(username='olafyxyz')).order_by(
        'twitter_media_id')
    db_count = db_user_objects.count()
    nss_images = db_user_objects.reverse()[:number_of_result]

    try:
        handle = '@' + request.user.social_auth.get(provider='twitter').extra_data['access_token']['screen_name']
    except:
        handle = ''

    context = {
        'media': nss_images,
        'n': number_of_result,
        'db_count': db_count,
        'handle': handle
    }
    return render(request, "demo.html", context)

def demo_view_vue(request, number_of_result=50):
    db_user_objects = img_link_storage.objects.filter(media_owner=User.objects.get(username='olafyxyz')).order_by(
        'twitter_media_id')
    db_count = db_user_objects.count()
    nss_images = db_user_objects.reverse()[:number_of_result]

    try:
        handle = '@' + request.user.social_auth.get(provider='twitter').extra_data['access_token']['screen_name']
    except:
        handle = ''

    context = {
        'media': nss_images,
        'n': number_of_result,
        'db_count': db_count,
        'handle': handle
    }
    return render(request, "demo-v.html", context)



def gallery_view(request, number_of_result=50):
    # check if user is logged in
    if not request.user.is_authenticated:
        return redirect('/')

    # fetch user media entry form db
    db_user_objects = img_link_storage.objects.filter(media_owner=request.user).order_by('twitter_media_id')
    db_max_id = db_user_objects.aggregate(Max('tweet_id'))['tweet_id__max']  # find last entry in db
    db_count = db_user_objects.count()
    nss_media = db_user_objects.reverse()[:number_of_result]

    # api access tokens
    tokens = request.user.social_auth.get(provider='twitter').extra_data['access_token']
    auth.set_access_token(tokens['oauth_token'], tokens['oauth_token_secret'])
    tweets = tw_api.user_timeline(tweet_mode="extended", since_id=db_max_id, count=100)  # get tweets from twitter api

    for tweet in tweets:
        if tweet.source == "Nintendo Switch Share":
            for extended_entity_media in tweet.extended_entities['media']:
                if extended_entity_media['type'] == 'photo':
                    db_entry = img_link_storage(media_owner=request.user,
                                                media_url=extended_entity_media['media_url_https'], tweet_id=tweet.id,
                                                media_type=extended_entity_media['type'],
                                                twitter_media_id=extended_entity_media['id'])
                    db_entry.save()
                elif extended_entity_media['type'] == 'video':
                    db_entry = img_link_storage(media_owner=request.user,
                                                media_url=get_largest_video(extended_entity_media), tweet_id=tweet.id,
                                                media_type=extended_entity_media['type'],
                                                vid_length=timedelta(milliseconds=extended_entity_media['video_info']['duration_millis']),
                                                vid_thumbnail_url=extended_entity_media['media_url_https'],
                                                twitter_media_id=extended_entity_media['id'])
                    db_entry.save()
                else:
                    continue

    context = {
        'media': nss_media,
        'n': number_of_result,
        'db_count': db_count,
        'handle': '@' + request.user.social_auth.get(provider='twitter').extra_data['access_token']['screen_name'],
    }

    return render(request, "gallery.html", context)


def img_view(request, media_id):
    db_img_obj = img_link_storage.objects.get(twitter_media_id=media_id)
    try:
        handle = '@' + request.user.social_auth.get(provider='twitter').extra_data['access_token']['screen_name']
    except:
        handle = ''
    context = {
        'img_link': db_img_obj.media_url,
        'media_type': db_img_obj.media_type,
        'tweet_id': db_img_obj.tweet_id,
        'handle': handle,
    }
    return render(request, 'imgview.html', context)


def about_view(request):
    try:
        handle = '@' + request.user.social_auth.get(provider='twitter').extra_data['access_token']['screen_name']
    except:
        handle = ''
    context = {
        'handle': handle,
    }
    return render(request, "about.html", context)


def logout(request):
    auth_logout(request)
    return redirect('/')


def privacy(request):
    try:
        handle = '@' + request.user.social_auth.get(provider='twitter').extra_data['access_token']['screen_name']
    except:
        handle = ''
    context = {
        'handle': handle,
    }
    return render(request, "privacy.html", context)


def shutdown_notice(request):
    return render(request, "shutdown_notice.html")
