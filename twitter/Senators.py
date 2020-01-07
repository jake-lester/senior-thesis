#
import sys
import os
import pickle
from datetime import datetime
import tweepy
import twitter_credentials

# set up authorization
auth = tweepy.OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)

# make API #TODO put this guy in the place it needs to be and then just pass auth as an arg
API = tweepy.API(auth)


class Senators():
    """
    class to help with transformin raw senator data into list of twitter user-ids
    also does other things, like make list of user objects
    """

    def __init__(self, senators_filename="senators.txt", run_all=False, api=False):
        self.senator_screen_names = []
        self.senator_user_ids = []
        self.senator_objects = []
        self.api = api
        if run_all:
            assert senators_filename
            self.run_all(senators_filename)

    def load_data(self, senators_filename="senators.txt"):
        senators_file = open(senators_filename, 'r')
        return senators_file

    def update_senator_screen_name_list(self, line):
        lst = line.split(" ")
        screen_name = lst[-1][:-1]  # remove \n
        self.senator_screen_names.append(screen_name)

    def make_senator_list(self, senators_file):
        # first transformation
        for line in senators_file.readlines():
            self.update_senator_screen_name_list(line)

    def update_senator_user_object_list(self, handle):
        if handle == "N/A":
            return
        else:
            self.senator_objects.append(self.api.get_user(handle))

    def make_senator_user_object_list(self, senator_screen_names=None):
        # returns list of twitter user objects given list
        if senator_screen_names is None:
            senator_screen_names = self.senator_screen_names

        for handle in senator_screen_names:
            self.update_senator_user_object_list(handle)

    def run_all(self, senators_filename):
        d = self.load_data(senators_filename)
        self.make_senator_list(d)
        self.make_senator_user_object_list()
        self.make_senator_user_id_list()

    def save_data_pickle(self, data, fpn):

        assert (fpn[-4:] == ".dat"), fpn
        with open(fpn, "wb") as f:
            pickle.dump(data, f)

    def load_data_pickle(self, fpn):
        assert (fpn[-4:] == ".dat"), fpn
        with open(fpn, "rb") as f:
            data = pickle.load(f)
        return data

    def update_senator_user_id_list(self, user):
        self.senator_user_ids.append(user.id_str)

    def make_senator_user_id_list(self):
        for user in self.senator_objects:
            self.update_senator_user_id_list(user)


if __name__ == "__main__":
    # note: must be run from twitter\\ dir

    # s_fn = os.getcwd() + "\\senators\\senators.txt"
    s = Senators(run_all=True, api=API)
    print(s.senator_user_ids)

    # today = str(datetime.datetime.today().strftime('%d-%m-%Y'))
    # users_fpn = os.getcwd() + "\\output\\senator_users_" + today + ".dat"

    # s.save_data(s.senator_objects, users_fpn)

    # loaded_senators = s.load_data_pickle(users_fpn)
    # print(loaded_senators[0])
