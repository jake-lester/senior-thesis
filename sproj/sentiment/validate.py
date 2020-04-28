import os
import json
import pandas as pd
#import nltk

#nltk.download('vader_lexicon')
#from nltk.sentiment.vader import SentimentIntensityAnalyzer

#sid = SentimentIntensityAnalyzer()

import sentiment
import clean_tweets


def load(fp):
    """
    Load csv data into dataframe
    """
    df = pd.read_csv(fp, names=["sentiment", "text"], usecols=[0, 5])
    return df


def score(df):
    df['nltk'] = [sentiment.make_sentiment(row['text'], model="nltk") for index, row in df.iterrows()]
    df['flair'] = [sentiment.make_sentiment(clean_tweets.remove_url_token(row['text']), model="flair") for index, row in df.iterrows()]
    #df['nltk'] = [convert_score(sentiment.make_sentiment(row['text'], model="nltk")) for index, row in df.iterrows()]
    #df['flair'] = [convert_score(sentiment.make_sentiment(clean_tweets.remove_url_token(row['text'])), model="flair") \
    #               for index, row in df.iterrows()]
    return df


def convert_score(value):
    """
    converts predicted sentiment value [-1:1] -> {0, 2, 4}
    """
    return round(value + 1) * 2

def convert_all_scores(df):
    df['nltk_c'] = [convert_score(row['nltk']) for index,row in df.iterrows()]
    df['flair_c'] = [convert_score(row['flair']) for index,row in df.iterrows()]
    return df


def calculateMSE(df):
    """Mean Squared Error"""
    from sklearn.metrics import mean_squared_error
    y_0 = df["sentiment"].values
    y_1 = df["prediction"].values
    return mean_squared_error(y_0, y_1)


#DF = loadAllData("data\\testdata.manual.2009.06.14.csv")
#DF = makePredictions(DF)
#print(calculateMSE(DF))


def loadAllDataFromDirectory(dir):
    j_files = [x for x in os.listdir(dir)]
    data = {}
    for j_file in j_files:
        with open(os.getcwd() + "\\dir\\" + j_file) as f:
            data.update(json.load(f))
    return data


def loadOneData(j_file):
    data = {}
    with open(os.getcwd() + "\\" + j_file) as f:
        data.update(json.load(f))
    return data


def makeDataFrame(data):
    d = {}
    d['Tweet_ID'] = [int(x) for x in list(data.keys())]
    d['created_at'] = [data[str(k)]['created_at'] for k in d['Tweet_ID']]
    d['user_id'] = [data[str(k)]['user_id'] for k in d['Tweet_ID']]
    d['text'] = [data[str(k)]['text'] for k in d['Tweet_ID']]
    d['is_quoted'] = [data[str(k)]['is_quoted'] for k in d['Tweet_ID']]
    d['quoted_id'] = [data[str(k)]['quoted_id'] for k in d['Tweet_ID']]
    df = pd.DataFrame(d, index=d['Tweet_ID'])
    df = df.drop(labels="Tweet_ID", axis=1)
    return df


def includeSentiment(df):
    df['compound_sentiment'] = [sid.polarity_scores(row.text)['compound'] for index, row in df.iterrows()]
    return df


def write2csv(df, fp):
    df.to_csv(fp)


if __name__ == "__main__":
    df = load("data\\sentiment140.csv")
    print(df.head())
    df = df.loc[df['sentiment']==2]
    print(df.head())
    #print(df.head())
    df = score(df)
    #print(df.head())
    df = convert_all_scores(df)
    #print(df.head())
    write2csv(df, "data\\validateSentimentBig.csv")

