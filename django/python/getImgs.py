import tweepy
from api_key import *

#api tokens
auth = tweepy.OAuthHandler(consumer_key, consumer_key_secret)
#user_oauth tokens (key, key_secret)
auth.set_access_token(olafyxyz_access_key, olafyxyz_access_key_secret)

api = tweepy.API(auth)


public_tweets = api.user_timeline(tweet_mode="extended")

#lists of twitter meida url with "Nintendo Switch Share" as source
nssImgs_status_id = []
nssImgs_url = []

for tweet in public_tweets:
    if tweet.source == "Nintendo Switch Share":
        for img_url in tweet.extended_entities['media']:
            if img_url['type'] == 'photo':
                nssImgs_status_id.append(tweet.id)
                nssImgs_url.append(img_url['media_url'])
            else:
                continue

print(nssImgs_status_id)
print(nssImgs_url)

#verify if the lengths of both lists are the same
if len(nssImgs_status_id) == len(nssImgs_url):
    print("Length of lists are equal:" + str(len(nssImgs_status_id)))
else:
    print("length of nssImgs_status_id = " + str(len(nssImgs_status_id)) + ", " + "length of nssImgs_url = " + str(len(nssImgs_url)))
            

