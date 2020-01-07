#
import sys
import os
import pickle
import datetime

sys.path.appendn (os.getcwd() + "\\parameters")
dirpath = os.getcwd().split("\\")


# this stuff should be under twitter parent dir in a main
import tweepy
import twitter_credentials

auth = tweepy.OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)


class Senators():
    """
    Deals with the 2step transformation of
        senators.txt
        -> ndarray(100,4) [state, firstname, lastname, handle]
        -> ndarray(100,4) [state, firstname, lastname, handle, userID]
    """

    def __init__(self, senators_filename=False, run_all=False, api=False):
        self.senator_screen_names = []
        self.senator_user_ids = []
        self.senator_objects = []
        self.api=api
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

    def save_data(self, data, fpn):

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

    def make_senator_user_id_list(self, user_object_list):
        for user in user_object_list:
            self.update_senator_user_id_list(user)


if __name__ == "__main__":
    # note: must be run from twitter\\ dir

    s_fn = os.getcwd() + "\\senators\\senators.txt"
    s = Senators(senators_filename=s_fn, run_all=True)
    print(s.senator_objects[0])

    today = str(datetime.datetime.today().strftime('%d-%m-%Y'))
    users_fpn = os.getcwd() + "\\output\\senator_users_" + today + ".dat"

    s.save_data(s.senator_objects, users_fpn)

    loaded_senators = s.load_data_pickle(users_fpn)
    print(loaded_senators[0])