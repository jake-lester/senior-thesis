import os
import json
import pandas as pd
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
sid = SentimentIntensityAnalyzer()


def loadAllData():
    j_files = [x for x in os.listdir(os.getcwd()+"\\data\\")]
    data = {}
    for j_file in j_files:
        with open(os.getcwd()+"\\data\\"+j_file) as f:
            data.update(json.load(f))
    return data

def loadAllDataFromDirectory(dir):
    j_files = [x for x in os.listdir(dir)]
    data = {}
    for j_file in j_files:
        with open(os.getcwd()+"\\dir\\"+j_file) as f:
            data.update(json.load(f))
    return data

def loadOneData(j_file):
    data = {}
    with open(os.getcwd()+"\\"+j_file) as f:
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
    data = loadAllData()
    df = makeDataFrame(data)
    df = includeSentiment(df)
    write2csv(df, os.getcwd()+"\\tweets.csv")
    print(df)