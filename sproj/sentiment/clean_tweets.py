## clean_tweets.py

import re

def remove_url_token(text):
    #s1 = re.sub(r'^https?:\/\/.*[\r\n]*', '', text)
    s2 = re.sub(r'http\S+', '', text)
    return s2
def remove_all_urls(tweets_df):
    tweets_df['text'] = [remove_url_token(row['text']) for index, row in tweets_df.iterrows()]
    return tweets_df