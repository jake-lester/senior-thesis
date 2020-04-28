## load.py #todo change to better naming

import database.fetch as fetch
import pandas as pd
import numpy as np
from sklearn import preprocessing
from decimal import Decimal


def fetch_data():
    # Fetch data from DB
    vix_df = fetch.fetch_vix()
    spx_df = fetch.fetch_spx()
    tweet_df = fetch.fetch_tweets()
    user_df = fetch.fetch_users()
    return vix_df, spx_df, tweet_df, user_df


def rename_fin_columns(vix_df, spx_df):
    vix_df = vix_df.rename(columns={'close': 'vix_close'})
    spx_df = spx_df.rename(columns={'close': 'spx_close'})
    return vix_df, spx_df


def remove_neutral_sentiment(tweet_df, model='nltk'):
    #tweet_df = tweet_df[tweet_df[model].abs() > thresh]
    #tweet_df[model] = [row[model] if True 0 if False for x for index, row in tweet_df.iterrows()]
    tweet_df[model] = tweet_df[model].replace(0, np.nan)
    return tweet_df


def weight_sentiment(tweet_df, user_df, sentiment_columns=['nltk','flair']):

    for user_id, row in user_df.iterrows():
        follower_count = row['total_followers']
        df = tweet_df.loc[tweet_df['user_id'] == user_id][sentiment_columns]
        for sentiment_column in sentiment_columns:
            df[sentiment_column] = df[sentiment_column] * Decimal((follower_count**(1./8)))
        df.index = df.index.astype('str')
        tweet_df.update(df)
    return tweet_df

def normalize(df, col):
    maxx = df[col].max()
    minn = df[col].min()
    df[col] = ((df[col] - minn)/(maxx - minn))
    df[col] = (df[col] - Decimal(.5))*2 #negative sentimen negative, postive postive

    return df

def prepare_data(senti_method=['nltk', 'flair'], remove_neutral_sent = True):
    vix_df, spx_df, tweet_df, user_df = fetch_data()
    if remove_neutral_sent:
        tweet_df = remove_neutral_sentiment(tweet_df)

    tweet_df = weight_sentiment(tweet_df, user_df)
    for s in senti_method:
        tweet_df = normalize(tweet_df, s)
    #tweet_df['score'] = tweet_df[senti_method]
    vix_df, spx_df = rename_fin_columns(vix_df, spx_df)
    return vix_df, spx_df, tweet_df

def make_flair_sentiment(tweet_df):
    tweet_df['flair'] = [sentiment.make_sentiment(txt, model='flair') for txt in tweet_df['text']]
    return tweet_df

if __name__ == "__main__":
    import sentiment.sentiment as sentiment
    import sentiment.clean_tweets as clean_tweets
    '''vix_df, spx_df, tweet_df, user_df = fetch_data()
    tweet_df2 = tweet_df.copy(deep=True)
    tweet_df = weight_sentiment(tweet_df, user_df)
    tweet_df = normalize(tweet_df, "flair")'''

    vix_df, spx_df, tweet_df, user_df = fetch_data()
    #tweet_df=tweet_df.head()
    tweet_df = clean_tweets.remove_all_urls(tweet_df)
    tweet_df = make_flair_sentiment(tweet_df)
    tweet_df.to_csv("tweets2.csv")
    #print(tweet_df.head())
    #tweet_df2['?score_matches'] = np.where(tweet_df['flair'] == tweet_df2['flair'], "True",
    #                                      "False")
    #print(tweet_df.loc[tweet_df2['?score_matches']=='False'])
    #print(tweet_df.loc[tweet_df2['?score_matches'] == 'True'])
