from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.models import Status
from tweepy import API

import twitter_credentials
import tweepy_filter_parameters
import datetime
import time
import json


class TwitterStreamer():
    """
    Class for streaming and processing live tweets
    """

    def stream_tweets(self, auth, filter_params, save_file, time_limit=False):
        # This handles Twitter authentication and the connection to the Twitter Streaming API
        # Input:
        # auth: twitter authorization
        # filter_params : dictionary containing words to track and accounts to follow
        # save_file : location to save tweets
        # stop_time : market hours default, otherwise stops after this many seconds

        track_list = filter_params["track_list"]
        follow_list = filter_params["follow_list"]
        async_bool = filter_params["async_bool"]

        ## moved to main #TODO put back here
        # auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
        # auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)

        api = API(auth)

        listener = MyStreamListener(save_file, time_limit, api)

        stream = Stream(auth, listener)

        # filter stream
        stream.filter(follow=follow_list, track=track_list, is_async=async_bool)


class MyStreamListener(StreamListener):  # inherits from StreamListener
    """
    listener class that writes fetched tweets to file until market close
    """

    def __init__(self, save_file, time_limit, api):
        self.save_file = open(save_file, 'a')
        self.time_limit = time_limit
        self.start_time = time.time()
        self.api = api

    def is_retweet(self, data):
        # ensures our streamer only gets tweets from our folow list, not responses to
        # inspired from @nelvintan tweepy issues 981
        data_dict = json.loads(data)
        return data_dict['text'][0:4] == "RT @"

    def from_creator(self, status):
        # taken from @nelvintan tweepy issues 981

        if hasattr(status, 'retweeted_status'):
            return False
        elif status.in_reply_to_status_id != None:
            return False
        elif status.in_reply_to_screen_name != None:
            return False
        elif status.in_reply_to_user_id != None:
            return False
        else:
            return True

    def on_data(self, data):

        # writes data to save_file if market hours or by time limit
        status = Status.parse(self.api, json.loads(data))
        #print(status)


        if not self.time_limit:
            print("broken")
            if datetime.now().hour >= 16:  # market is closed at 16:00
                self.save_file.close()
                return False
            elif not self.from_creator(status):
                return True
            # TODO currently not writing any tweets but that might be because there aren't any senator tweets
            else:
                try:
                    self.save_file.write(data)
                    return True
                except BaseException as e:
                    print("Error on_data: %s" % str(e))
            return True
        else:
            if self.time_limit <= time.time() - self.start_time:
                self.save_file.close()
                return False
            elif not self.from_creator(status):
                return True
            else:
                try:
                    self.save_file.write(data)
                    return True
                except BaseException as e:
                    print("Error on_data: %s" % str(e))
            return True

    def on_error(self, status):
        if status == 420:
            # returning False in on_data disconnects the stream
            return False
