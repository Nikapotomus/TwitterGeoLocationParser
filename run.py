from twython import Twython
import datetime
import time
import sys
import csv
import simplekml

import subprocess

twitter_username = "Nikapotomus"

def output_path_gen():
    # print ">>> Generating CSV file"
    ts = time.time()
    myTimestamp = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y_%H-%M-%S')

    #save in a folder called kml_files
    newFileName = "kml_files/"+twitter_username+'-'+myTimestamp+'.kml'

    # bashCmd = 'touch kml_files/{}'.format(newFileName)
    # subprocess.call(bashCmd, shell=True)

    return newFileName


''' Go to https://apps.twitter.com/ to register for api keys '''
CONSUMER_KEY = ''
CONSUMER_SECRET = ''

ACCESS_KEY = ''
ACCESS_SECRET = ''

twitter = Twython(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_KEY,ACCESS_SECRET)

# Gets the latest tweet id
latest_tweet_id = twitter.get_user_timeline(
    screen_name=twitter_username,
    count=1)

if latest_tweet_id is None:
    print(">>> ERROR: Could not find latest tweet!")
    sys.exit()

LT_ID = latest_tweet_id[0]["id"] ## cache tweet id to not do pointless requests
geo_location_tweets = []

#create kml object to store results
kml=simplekml.Kml()

# for i in range(0, 1): ## iterate through all tweets
# tweet extract method with the last list item as the max_id
user_timeline = twitter.get_user_timeline(screen_name= twitter_username,
    count=200,
    include_retweets=False,
    max_id=LT_ID)

# time.sleep(300) ## 5 minute rest between api calls
# print(">>>> DEBUG: {} ").format(user_timeline)

for tweet in user_timeline:
    #checks if there is a geo location returned
    if tweet['coordinates'] is None:
        continue

    print(">>> Tweet id {} has geo data!").format(tweet["id"])
    # print(tweet)
    geo_location_tweets.append(tweet) # append tweet id's

print(">>> Pushing coordinates to kml file")

for geo_tweet in geo_location_tweets:
    kml.newpoint(name=geo_tweet["created_at"],
        description=geo_tweet["text"],
        coords=[(geo_tweet["coordinates"]["coordinates"][0],
            geo_tweet["coordinates"]["coordinates"][1])])

kml.save(output_path_gen())
print(">>> Successfully created kml log file!")
