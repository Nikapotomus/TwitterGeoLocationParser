from twython import Twython
import datetime
import time
import sys
import simplekml

import version
from config import TGLP_Config

print version.__banner__
print "-"*40

# twitter_username = TGLP_Config.target_twitter_username
twitter_username = raw_input("Enter the twitter username to investigate:\n")

while True:
    try:
        number_of_pull_cycles = int(float(raw_input("Enter the number of tweets to pull:\n"))) / 200
    except ValueError:
        print("Invalid input, please a valid number.")
        continue
    else:
        break

#increments in multiples of 16 (api request limit per 5 mins)
#and calculates the number of pulls required to the closest 16 multiple
for i in range(15,1000,15):
    if number_of_pull_cycles <= i:
        number_of_pull_cycles = i
        break

print("-"*40)
print(">>> Getting {}'s tweets over {} requests").format(twitter_username, number_of_pull_cycles)

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

for i in range(0, number_of_pull_cycles): ## iterate through all tweets
# tweet extract method with the last list item as the max_id
    user_timeline = twitter.get_user_timeline(screen_name= twitter_username,
        count=200,
        include_retweets=False,
        max_id=LT_ID[-1])

    # print(">>> Searching for a max id of {}").format(LT_ID[-1])
    # print(">>> Successfully gathered {} tweets").format(len(user_timeline))

    # if i == 0:
    #     continue
    # if i % 16 == 0:
    #     print("+++ 16 request API limit hit on cycle num {}, 5 minrest").format(i)
    #     time.sleep(300)

    for tweet in user_timeline:
        #add the tweets checked to the array
        LT_ID.append(tweet["id"])

        #checks if there is a geo location returned
        if tweet['coordinates'] is not None:
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

def output_path_gen():
    ts = time.time()
    myTimestamp = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y_%H-%M-%S')

    #save in a folder called kml_files
    newFileName = "kml_files/"+twitter_username+'-'+myTimestamp+'.kml'
    return newFileName

kml.save(output_path_gen())
print(">>> Successfully created kml log file!")
