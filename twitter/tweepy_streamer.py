import datetime
import time
import json

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.models import Status
from tweepy import API


class TwitterStreamer():
    """
    Class for streaming and processing live tweets
    """

    def start_stream(self, cred, filter_params, save_fp, stop_cond):
        # This handles Twitter authentication and the connection to the Twitter Streaming API
        # Input:
        # cred: dictionary containing credentials: consumer key, consumer secret key, access token, access token secret
        # filter_params : dictionary containing words to track and accounts to follow
        # save_fp : location to save tweets file
        # stop_cond : when to stop streaming.
        #   'never' : never stop. Not recomended
        #   'market' : stop if not market hours
        #   int : stop after this many seconds.

        track_list = filter_params["track_list"]
        follow_list = filter_params["follow_list"]
        async_bool = filter_params["async_bool"]

        auth = OAuthHandler(cred["consumer key"], cred["consumer secret"])
        auth.set_access_token(cred["access token"], cred["access token secret"])
        print("auth set up")

        #api = API(auth)
        #print("api set up")

        # convert user screenames to user ids
        #follow_list = self.screenname2userid(api, follow_list)
        print("follow list complete")

        listener = MyStreamListener(save_fp, stop_cond)
        print("listener set up")
        stream = Stream(auth, listener)
        print("stream set up")

        # filter stream
        stream.filter(follow=follow_list, track=track_list, is_async=async_bool)

    def screenname2userid(self, api, follow_list):
        # takes list of screen names and returns coresponding user ids
        user_ids = [api.get_user(handle).id_str for handle in follow_list]
        #print("done with screename2userid")
        #print("user ids:", user_ids)
        return user_ids


def from_creator(status):
    # taken from @nelvintan tweepy issues 981
    # ensures we only grab tweets from original creator on follow list
    print("from creator ran")
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


class MyStreamListener(StreamListener):  # inherits from StreamListener
    """
    listener class that writes fetched tweets to file until market close
    """

    def __init__(self, save_fp, stop_cond, api=None):
        print("initialized")
        self.save_file = open(save_fp, 'a')
        self.stop_cond = stop_cond
        self.start_time = time.time()
        self.api = api or API()
        print("done initializing")

    def on_data(self, data):
        # writes data to save_file if market hours or by time limit
        # return False to exit stream, True to continue
        print("got to here")
        status = Status.parse(self.api, json.loads(data))
        print("on data")
        if self.stop_cond is int:
            elapsed_time = time.time() - self.start_time
            print("elapsed time: ", elapsed_time, "seconds")
            if elapsed_time >= self.stop_cond:
                self.save_file.close()
                print("done streaming")
                return False
            elif not from_creator(status):
                print("not from user")
                return True
            else:
                try:
                    self.save_file.write(data)
                    print("Wrote tweet")
                    return True
                except BaseException as e:
                    print("Error on_data: %s" % str(e))
            return True

        elif self.stop_cond == "market":
            print("market")
            if datetime.now().hour >= 16:  # market is closed at 16:00
                self.save_file.close()
                return False
            elif not from_creator(status):
                return True
            else:
                try:
                    self.save_file.write(data)
                    print("wrote tweet")
                    return True
                except BaseException as e:
                    print("Error on_data: %s" % str(e))
            return True

        elif self.stop_cond == 'never':
            try:
                self.save_file.write(data)
                print("Wrote tweet")
                return True
            except BaseException as e:
                print("Error on_data: %s" % str(e))
            return True

        else:
            print("error")
            assert False, "stop_cond is invalid %s" % str(self.stop_cond)

    def on_error(self, status):
        if status == 420:
            # returning False in on_data disconnects the stream
            return False
