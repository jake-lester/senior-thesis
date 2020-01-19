from _datetime import datetime
import tweepy
import twitter_credentials
import tweepy_filter_parameters
from Senators import Senators
from tweepy_streamer import TwitterStreamer, MyStreamListener

# location to store streamed tweets
output_fp = "twitter\\output\\senators\\"

# make API #TODO put this guy in the place it needs to be and then just pass auth as an arg
now = datetime.now()

# senator specific stuff for follow list
s = Senators()
senator_text_file = s.load_data("twitter\\senators.txt")
screen_names = s.make_senator_list(senator_text_file)

screen_names = [handle for handle in screen_names if handle != "N/A"]
# stream filter parameters
filter_params = {
    "follow_list": screen_names,  # tweepy_filter_parameters.FOLLOW,
    "track_list": tweepy_filter_parameters.TRACK,
    "async_bool": tweepy_filter_parameters.IS_ASYNC
}

# credentials
cred = {
    "consumer key": twitter_credentials.CONSUMER_KEY,
    "consumer secret": twitter_credentials.CONSUMER_SECRET,
    "access token": twitter_credentials.ACCESS_TOKEN,
    "access token secret": twitter_credentials.ACCESS_TOKEN_SECRET
}

# init streamer
today = str(datetime.today().strftime('%d-%m-%Y'))
print("Commencing Stream on ", today)

# make file if not exist
save_fp = output_fp + today + ".json"
f = open(save_fp, "w+")
f.close()

# start stream
twitter_streamer = TwitterStreamer()
twitter_streamer.start_stream(cred, filter_params, save_fp, stop_cond=60)
# print("Done Streaming")
