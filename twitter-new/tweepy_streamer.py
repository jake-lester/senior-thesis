from __future__ import absolute_import, print_function

import twitter_credentials as tc
from tweepy import OAuthHandler, Stream, StreamListener

from tweepy.models import Status
from tweepy import API

import time
import json
import pprint

# Go to http://apps.twitter.com and create an app.
# The consumer key and secret will be generated for you after
consumer_key = tc.CONSUMER_KEY
consumer_secret = tc.CONSUMER_SECRET

# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section
access_token = tc.ACCESS_TOKEN
access_token_secret = tc.ACCESS_TOKEN_SECRET


class StdOutListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """

    def __init__(self, save_fp=None, stop_cond=None, api=None):
        self.start_time = time.time()
        #open(save_fp,'w').close() #empty file first
        #self.save_file = open(save_fp, 'a', encoding="utf-8")
        #self.save_file.write("[")

        self.save_fp = save_fp

        self.stop_cond = stop_cond
        self.api = api
        self.data={}

    """
    def on_data(self, data):
        #status = Status.parse(self.api, json.loads(data))
        elapsed_time = time.time() - self.start_time
        print("elapsed time: ", elapsed_time, "seconds")
        if elapsed_time >= self.stop_cond:
            self.save_file.close()
            return False
        #elif not from_creator(status):
        #    #self.save_file.close()
        #    return True
        #self.save_file.write(data)
        #return True

        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(json.loads(data))
        print(type(json.loads(data)))
        print(json.loads(data).keys())
        print(json.loads(data)['retweeted_status'])

        return False

    """

    def on_status(self, status):
        elapsed_time = time.time() - self.start_time
        print("elapsed time ", elapsed_time, "seconds")
        # print(status._json.keys())
        if elapsed_time >= self.stop_cond:
            #self.save_file.write(self.data)

            with open(self.save_fp, 'w') as fout:
                json.dump(self.data, fout)
            fout.close()
            return False
        elif not from_creator(status):
            #print("not from creator", status)
            return True
        #print(status._json['user']['screen_name'])

        tweet_id,tweet_data = parse_tweet(status)

        self.data[tweet_id] = tweet_data
        return True






    def on_error(self, status):
        if status == 420:
            # returning False in on_data disconnects the stream
            return False

def parse_tweet(status):
    try:
        text = status.extended_tweet["full_text"]
        #reply_count = status.extended_tweet["reply_count"]
        #retweet_count = status.extended_tweet["full_text"]
        #favorite_count = status.extended_tweet["full_text"]
    except AttributeError:
        text = status.text

    user_name = status._json['user']['screen_name']
    user_followers = status._json['user']['followers_count']
    tweet_id = status._json['id']
    time_stamp = status._json['created_at']

    tweet_data = {"created_at": time_stamp,
                  "followers_count" : user_followers,
                  "text" : text,
                  "screen_name": user_name}

    return tweet_id, tweet_data

def from_creator(status):
    # taken from @nelvintan tweepy issues 981
    # ensures we only grab tweets from original creator on follow list
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


if __name__ == '__main__':
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = API(auth)

    l = StdOutListener(save_fp="output\\new_sample_tweet.json", stop_cond=8, api=api)

    stream = Stream(auth, l)
    stream.filter(track=['basketball'])
