import json
import pprint
fp = "twitter-new\\output\\new_sample_tweet.json"

with open(fp) as j:

    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(json.load(j))

