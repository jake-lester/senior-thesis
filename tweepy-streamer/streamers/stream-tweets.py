#!/usr/bin/env python
# tweepy-streamer\streamers\stream-tweets

from tweepy import Stream, StreamListener
import time
import json
import logging
import pandas as pd
import os
from datetime import datetime
from urllib3 import exceptions

from config import create_api

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

SAVE_NO=100


class StdOutListener(StreamListener):
    """
    A listener that handles tweets received from the stream.
    This one filters by key word and makes custom output.
    """

    def __init__(self, api, save_fp, stop_cond):
        self.start_time = time.time()
        self.save_fp = save_fp
        #self.save_no=SAVE_NO
        self.stop_cond = stop_cond
        self.api = api
        self.data = {}

    def on_status(self, status):
        global SAVE_NO
        logger.info(f"Processing tweet id {status.id}")
        elapsed_time = time.time() - self.start_time
        if elapsed_time >= self.stop_cond:
            with open(self.save_fp+str(SAVE_NO)+".json", 'w') as fout:
                json.dump(self.data, fout)
            fout.close()
            print("saved to ", SAVE_NO)
            SAVE_NO += 1
            self.start_time = time.time()
            self.data={}

        if not from_creator(status):
            return True
        tweet_id, tweet_data = parse_tweet(status)
        self.data[tweet_id] = tweet_data
        return True

    def on_error(self, status):
        if status == 420:
            # returning False in on_data disconnects the stream
            return False


def parse_tweet(status):
    #print(status)
    try:
        text = status.extended_tweet["full_text"]
    except AttributeError:
        text = status.text

    #user_name = status._json['user']['screen_name']
    user_id = status._json['user']['id']
    #user_followers = status._json['user']['followers_count']
    tweet_id = status._json['id']
    time_stamp = status._json['created_at']
    #is_quote = hasattr(status._json, "quoted_status_id")
    try:
        quoted_status_id = status._json['quoted_status_id']
        is_quote = True
    except:
        quoted_status_id = None
        is_quote = False
    #quote_count = status._json['quote_count']
    #reply_count = status._json['reply_count']
    #retweet_count = status._json['retweet_count']
    #favorite_count = status._json['favorite_count']
    #is_retweet=
    #retweet_id =
    """
    is_retweet
    quoted_status_id
    quoted_status["""

    tweet_data = {"created_at": time_stamp,
                  #"followers_count": user_followers,
                  #"screen_name": user_name,
                  "user_id": user_id,
                  "text": text,
                  "is_quoted" : is_quote,
                  "quoted_id" : quoted_status_id
                  #"quote_count": quote_count,
                  #"reply_count": reply_count,
                  #"retweet_count": retweet_count,
                  #"favorite_count": favorite_count

                  }

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


def main(save_fp, time_limit, keywords=None, accountstofollow=None):
    global SAVE_NO
    api = create_api()
    tweets_listener = StdOutListener(api, save_fp, time_limit)
    stream = Stream(api.auth, tweets_listener)
    while True:
        try:
            stream.filter(follow=accountstofollow, stall_warnings=True)
        except exceptions.ProtocolError:
            SAVE_NO += 1
            print("!!!!! EXCEPTION !!!!!!")
            continue


if __name__ == "__main__":
    '''
    NOTE!
    includes retweets of people in the list. post filtering is required for user ids not in our base'''


    today = str(datetime.today().strftime('%d-%m-%Y'))
    print("Commencing Stream on ", today)
    # make file if not exist
    # todo make sure file doesnt exist
    save_fp = "tweepy-streamer\\tweet_output\\"
    #try:
    #    open(save_fp)
    #    print(save_fp, "already exists. Not running to avoid overwrite")
    #except:
    #f = open(save_fp, "w+")
    #f.close()
    df = pd.read_csv("tweepy-streamer\\finAccounts.csv")
    accnts = df.Twitter_ID.values
    accnts = [str(x) for x in accnts]
    #accnts.append("1193623572570345473")
    #return
    main( save_fp, 900, accountstofollow=accnts)
    #save every 15 minutes

