#!/usr/bin/env python
# tweepy-streamer\streamers\stream-tweets

from tweepy import Stream, StreamListener
import time
import json
import logging

from config import create_api

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


class StdOutListener(StreamListener):
    """
    A listener that handles tweets received from the stream.
    This one filters by key word and makes custom output.
    """

    def __init__(self, api, save_fp, stop_cond):
        self.start_time = time.time()
        self.save_fp = save_fp
        self.stop_cond = stop_cond
        self.api = api
        self.data = {}

    def on_status(self, status):
        logger.info(f"Processing tweet id {status.id}")
        elapsed_time = time.time() - self.start_time
        if elapsed_time >= self.stop_cond:
            with open(self.save_fp, 'w') as fout:
                json.dump(self.data, fout)
            fout.close()
            return False

        elif not from_creator(status):
            return True

        tweet_id, tweet_data = parse_tweet(status)
        self.data[tweet_id] = tweet_data
        return True

    def on_error(self, status):
        if status == 420:
            # returning False in on_data disconnects the stream
            return False


def parse_tweet(status):
    try:
        text = status.extended_tweet["full_text"]
    except AttributeError:
        text = status.text

    user_name = status._json['user']['screen_name']
    user_followers = status._json['user']['followers_count']
    tweet_id = status._json['id']
    time_stamp = status._json['created_at']

    tweet_data = {"created_at": time_stamp,
                  "followers_count": user_followers,
                  "text": text,
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


def main(keywords, save_fp, time_limit):
    api = create_api()
    tweets_listener = StdOutListener(api, save_fp, time_limit)
    stream = Stream(api.auth, tweets_listener)
    stream.filter(track=keywords)


if __name__ == "__main__":
    main(["basketball"], "streamers\\output\\new_sample_tweet.json", 8)
