import tweepy
from api_key import *

auth = tweepy.OAuthHandler(consumer_key, consumer_key_secret)
auth.set_access_token(olafyxyz_access_key, olafyxyz_access_key_secret)

api = tweepy.API(auth)
tweet = api.get_status(id='1323368879641354240', tweet_mode="extended")
tweet_media = tweet.extended_entities['media'][0]


print(tweet_media)
# vid_variants = {}
# for vid in tweet_media['video_info']['variants']:
#     if not vid['content_type'] == 'video/mp4':
#         continue
#     else:
#         vid_variants[vid['bitrate']] = vid['url']
# print(vid_variants[max(vid_variants.keys())])

# #lists of twitter meida url with "Nintendo Switch Share" as source
# nssImgs_status_id = []
# nssImgs_url = []
# public_tweets = api.user_timeline(tweet_mode="extended", count=10)
#
# for tweet in public_tweets:
#     if tweet.source == "Nintendo Switch Share":
#         for img_url in tweet.extended_entities['media']:
#             #print(type(img_url))
#             if img_url['type'] == 'photo':
#                 nssImgs_status_id.append(tweet.id)
#                 nssImgs_url.append(img_url['media_url'])
#             else:
#                 continue
#
# print(len(nssImgs_url))
