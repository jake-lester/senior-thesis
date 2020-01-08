from _datetime import datetime
import tweepy
import twitter_credentials
import tweepy_filter_parameters
import Senators

from tweepy_streamer import TwitterStreamer, MyStreamListener

# set up authorization
auth = tweepy.OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)

# location to store streamed tweets
output_fp = "senator_tweets"

# make API #TODO put this guy in the place it needs to be and then just pass auth as an arg
now = datetime.now()

# stream filter parameters
filter_params = {
    "follow_list": tweepy_filter_parameters.FOLLOW,
    "track_list": tweepy_filter_parameters.TRACK,
    "async_bool": tweepy_filter_parameters.IS_ASYNC
}

# Check if market is open
if now.hour < 10 and now.minute < 30:
    print("Market is not yet open")
elif now.hour > 16:
    print("Market is closed")
else:
    print("Market is open")

# start stream
today = str(datetime.today().strftime('%d-%m-%Y'))
print("Commencing Stream on ", today)

save_file = output_fp+"\\" + today + ".json"
f = open(save_file, "w+")
f.close()
time_limit= 240
twitter_streamer = TwitterStreamer()

# set time_limit or just use market hours
twitter_streamer.stream_tweets(auth, filter_params, save_file, time_limit=time_limit)
#print("Done Streaming")
