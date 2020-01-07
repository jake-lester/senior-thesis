from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API

import twitter_credentials
import tweepy_filter_parameters
import datetime


class TwitterStreamer():
    """
    Class for streaming and processing live tweets
    """

    def stream_tweets(self, auth, filter_params, save_file):
        # This handles Twitter authentication and the connection to the Twitter Streaming API
        # Input:
        # auth: twitter authorization
        # filter_params : dictionary containing words to track and accounts to follow

        track_list = filter_params["track_list"]
        follow_list = filter_params["follow_list"]
        async_bool = filter_params["async_bool"]

        ## moved to main
        # auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
        # auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)

        listener = MyStreamListener(save_file)

        stream = Stream(auth, listener)

        # filter stream
        stream.filter(follow=follow_list, track=track_list, is_async=async_bool)


class MyStreamListener(StreamListener):  # inherits from StreamListener
    """
    listener class that writes fetched tweets to file until market close
    """

    def __init__(self, save_file):
        self.save_file = save_file

    def on_data(self, data):
        # writes data to save_file if market hours
        if datetime.now().hour >= 16: #market is closed at 16:00
            self.save_file.close()
            return False
        else:
            try:
                with open(self.save_file, 'a') as tf:
                    tf.write(data)
                return True
            except BaseException as e:
                print("Error on_data: %s" % str(e))
        return True

    def on_error(self, status):
        if status == 420:
            # returning False in on_data disconnects the stream
            return False


if __name__ == "__main__":
    hash_tag_list = ["donald trump", "hillary clinton"]
    follow_list = [tweepy_filter_parameters.SENATOR_HANDLES[0]]
    fetched_tweets_filename = "../output/tweets.json"

    twitter_streamer = TwitterStreamer()
    twitter_streamer.stream_tweets(fetched_tweets_filename,
                                   hash_tag_list=hash_tag_list)  # , follow_list=["@realDonaldTrump"])
