import os
import json
import nltk

nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer

sid = SentimentIntensityAnalyzer()

def loadAllDataFromDirectory(dir):
    j_files = [x for x in os.listdir(dir)]
    data = {}
    for j_file in j_files:
        with open(dir+"\\"+j_file) as f:
            data.update(json.load(f))
    return data

def parseTwitterDate(created_at):
    """
    TODO move this into different module. It is very generic and should be lower level
    """
    month_dict = {'Jan': '01',
                  'Feb': '02',
                  'Mar': '03',
                  'Apr': '04',
                  'May': '05',
                  'Jun': '06',
                  'Jul': '07',
                  'Aug': '08',
                  'Sep': '09',
                  'Oct': '10',
                  'Nov': '11',
                  'Dec': '12'}
    dlst = created_at.split(' ')
    return '-'.join([dlst[5], month_dict[dlst[1]], dlst[2]]) + ' ' + dlst[3]

def sentiScore(text):

    return sid.polarity_scores(text)['compound']

def none2Null(val):
    if val == 'None':
        return None #"NULL"
    return val

def debug():
    """legacy should todo be removed"""
    tweet_fp = 'output'
    dir = str(os.getcwd()) +"\\tweepy-streamer\\streamers\\"+tweet_fp+"\\"
    j_files = [x for x in os.listdir(dir)]

    for j_file in j_files:
        data = {}
        with open(dir+"\\" + j_file) as f:
            data.update(json.load(f))

        try:
            val = [
                (key,
                 parseTwitterDate(value['created_at']),
                 str(value['user_id']),
                 value['text'],
                 value['is_quoted'],
                 none2Null(str(value['quoted_id'])),
                 sentiScore(value['text']))
                for key, value in data.items()]
        except:
            print(j_file)