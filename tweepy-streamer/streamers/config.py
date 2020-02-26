# tweepy-streamer\streamers\config.py

import tweepy
import logging
import os

logger = logging.getLogger()


def create_api():
    consumer_key = os.getenv("CONSUMER_KEY")
    consumer_secret = os.getenv("CONSUMER_SECRET")
    access_token = os.getenv("ACCESS_TOKEN")
    access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

    print('consumer_key', consumer_key)
    print("consumer_secret", consumer_secret)
    print("access_token", access_token)
    print("access_token_secret", access_token_secret)

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    try:
        api.verify_credentials()
    except Exception as e:
        logger.error("Error creating API", exc_info=True)
        raise e
    logger.info("API created")
    return api
