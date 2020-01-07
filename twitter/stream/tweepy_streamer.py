from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API

import twitter_credentials
import tweepy_filter_parameters

class TwitterStreamer():
    """
    Class for streaming and processing live tweets
    """

    def stream_tweets(self, fetched_tweets_filename, hash_tag_list=None, follow_list=None):
        # This handles Twitter authentication and the connection to the Twitter Streaming API
        # Input:
        # fetched_tweets_filename : file we want to write to
        # hash_tag_list : hashtags that we filter by"""

        listener = StdOutListener(fetched_tweets_filename)
        auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
        auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)

        stream = Stream(auth, listener)

        # filter stream
        stream.filter(track=hash_tag_list,follow=follow_list)
        stream.filter()


class StdOutListener(StreamListener):  # inherits from StreamListener
    """
    This is a basic listener class that writes recieved tweets to stdout
    """

    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    def on_data(self, data):
        #overidden method that takes data streamed in and prints out data
        '''
        try:
            with open(self.fetched_tweets_filename, 'a') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        '''
        print(data)
        return True

    def on_error(self, status):
        print(status)

def get_user_ids(screenames):
    auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
    auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)
    twitter_api = API(auth)


if __name__ == "__main__":

    hash_tag_list = ["donald trump", "hillary clinton"]
    follow_list = [tweepy_filter_parameters.SENATOR_HANDLES[0]]
    fetched_tweets_filename = "../output/tweets.json"

    twitter_streamer = TwitterStreamer()
    twitter_streamer.stream_tweets(fetched_tweets_filename, hash_tag_list=hash_tag_list)#, follow_list=["@realDonaldTrump"])

