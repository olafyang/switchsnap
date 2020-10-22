import tweepy
import json
from api_key import *


auth = tweepy.OAuthHandler(consumer_key, consumer_key_secret)
auth.set_access_token(olafyxyz_access_key, olafyxyz_access_key_secret)

api = tweepy.API(auth)

#lists of twitter meida url with "Nintendo Switch Share" as source
nssImgs_status_id = []
nssImgs_url = []
public_tweets = api.user_timeline(tweet_mode="extended", count=100)

for tweet in public_tweets:
    if tweet.source == "Nintendo Switch Share":
        for img_url in tweet.extended_entities['media']:
            if img_url['type'] == 'photo':
                nssImgs_status_id.append(tweet.id)
                nssImgs_url.append(img_url['media_url'])
            else:
                continue

print(len(nssImgs_url))