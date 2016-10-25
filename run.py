from twython import Twython
import datetime
import time
import sys
import csv
import simplekml
import subprocess

import version
from config import TGLP_Config

print version.__banner__
print "-"*40

twitter_username = TGLP_Config.target_twitter_username

print(">>> Requesting {} tweets").format(twitter_username)

def output_path_gen():
    # print ">>> Generating CSV file"
    ts = time.time()
    myTimestamp = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y_%H-%M-%S')

    #save in a folder called kml_files
    newFileName = "kml_files/"+twitter_username+'-'+myTimestamp+'.kml'

    # bashCmd = 'touch kml_files/{}'.format(newFileName)
    # subprocess.call(bashCmd, shell=True)
    return newFileName

CONSUMER_KEY = TGLP_Config.CONSUMER_KEY
CONSUMER_SECRET = TGLP_Config.CONSUMER_SECRET

ACCESS_KEY = TGLP_Config.ACCESS_KEY
ACCESS_SECRET = TGLP_Config.ACCESS_SECRET

twitter = Twython(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_KEY,ACCESS_SECRET)

# Gets the latest tweet id
latest_tweet_id = twitter.get_user_timeline(
    screen_name=twitter_username,
    count=1)

if latest_tweet_id is None:
    print(">>> ERROR: Could not find latest tweet!")
    sys.exit()

LT_ID = [latest_tweet_id[0]["id"]] ## cache tweet id to not do pointless requests
geo_location_tweets = []

#create kml object to store results
kml=simplekml.Kml()

for i in range(0, TGLP_Config.number_of_pull_cycles): ## iterate through all tweets
# tweet extract method with the last list item as the max_id
    user_timeline = twitter.get_user_timeline(screen_name= twitter_username,
        count=200,
        include_retweets=False,
        max_id=LT_ID[-1])

    # print(">>> Searching for a max id of {}").format(LT_ID[-1])
    # print(">>> Successfully gathered {} tweets").format(len(user_timeline))

    #time.sleep(300) #sleep inbetween requests for larger data sets

    for tweet in user_timeline:
        #add the tweets checked to the array
        LT_ID.append(tweet["id"])

        #checks if there is a geo location returned
        if tweet['coordinates'] is None:
            continue

        print(">>> Tweet id {} has geo data!").format(tweet["id"])
        # print(tweet)
        geo_location_tweets.append(tweet) # append tweet id's

print(">>> Parsed a total of {} tweets").format(len(LT_ID))
print(">>> Found {} geo location tweets").format(len(geo_location_tweets))
print(">>> Pushing coordinates to kml file")

for geo_tweet in geo_location_tweets:
    kml.newpoint(name=geo_tweet["created_at"],
        description=geo_tweet["text"],
        coords=[(geo_tweet["coordinates"]["coordinates"][0],
            geo_tweet["coordinates"]["coordinates"][1])])

kml.save(output_path_gen())
print(">>> Successfully created kml log file!")
