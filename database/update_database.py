import pandas as pd
import os
import json
import mysql.connector

from helper import loadAllDataFromDirectory, parseTwitterDate, sentiScore, none2Null

mysql=mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='password',
    database='midterm',
    auth_plugin='mysql_native_password'
)

mycursor=mysql.cursor()

def insertUsers(finAccounts_fp):
    sql = "insert into Users(user_id, twitter_handle, `rank`, popularity_rating, total_followers) Values(%s, %s, %s, %s, %s)"
    users_df = pd.read_csv(finAccounts_fp, header=0, index_col= 'Twitter_ID')
    val = [(index,
            row['Twitter Handle'],
            row['Rank'],
            row['Popularity Rating'],
            row['Total Followers']
            ) for index, row in users_df.iterrows()]
    #mycursor.executemany(sql, val)
    #mysql.commit()
    return users_df.index.values

def insertVIX(quotes_fp):
    sql = "insert into Vix_Data(`datetime`, `open`, `high`, `low`, `close`, `volume`) Values(%s, %s, %s, %s, %s, %s)"
    with open(quotes_fp,'r') as f:
        vix_data = json.load(f)['VIX']
    val = [(key,
            float(value['1. open']),
            float(value['2. high']),
            float(value['3. low']),
            float(value['4. close']),
            float(value['5. volume'])
            ) for key, value in vix_data.items()]
    #mycursor.executemany(sql, val)
    #mysql.commit()
    
def insertSPX(quotes_fp):
    sql = "insert into SPX_Data(`datetime`, `open`, `high`, `low`, `close`, `volume`) Values(%s, %s, %s, %s, %s, %s)"
    with open(quotes_fp, 'r') as f:
        spx_data = json.load(f)['SPX']
    val = [(key,
            float(value['1. open']),
            float(value['2. high']),
            float(value['3. low']),
            float(value['4. close']),
            float(value['5. volume'])
            ) for key, value in spx_data.items()]
    #mycursor.executemany(sql, val)
    #mysql.commit()

def insertTweets(dir, user_ids):
    sql = "insert into Tweets(`tweet_id`, `created_at`, `user_id`, `text`, `is_quoted`, `quoted_id`, `sentiment_score`) Values(%s, %s, %s, %s, %s, %s, %s)"
    tweet_data = loadAllDataFromDirectory(dir)

    val = [
        (key,
         parseTwitterDate(value['created_at']),
         str(value['user_id']),
         value['text'],
         value['is_quoted'],
         none2Null(str(value['quoted_id'])),
         sentiScore(value['text']))
        for key, value in tweet_data.items()
        if value['user_id'] in user_ids]

    mycursor.executemany(sql, val)
    mysql.commit()



if __name__ == "__main__":
    userhandles = insertUsers(str(os.getcwd())+"\\tweepy-streamer\\finAccounts.csv")
    for finData_fn in ["quotes06-03-2020.json", "quotes16-03-2020.json", "quotes22-03-2020.json"]:
        insertVIX(str(os.getcwd())+"\\stock_quotes\\"+finData_fn)
        insertSPX(str(os.getcwd()) + "\\stock_quotes\\" + finData_fn)

    for tweet_fp in ["output", "output2"]:
        insertTweets(str(os.getcwd()) +"\\tweepy-streamer\\streamers\\"+tweet_fp+"\\", userhandles)
