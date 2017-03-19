########################
'''
Things to fix:
Currently collects retweets, replies to user
'''
########################

from __future__ import absolute_import, print_function

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from auth import TwitterAuth

import json

consumer_key = TwitterAuth.consumer_key
consumer_secret = TwitterAuth.consumer_secret

access_token = TwitterAuth.access_token
access_token_secret = TwitterAuth.access_token_secret

fhOut =  open('output.json', 'w')

date_collect = input("Enter date to collect (Mar 18 2017): ")
date_collect = date_collect.split()

# Hard code months
months = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}

class PastDate(Exception):
    pass

class Listener(StreamListener):
    def on_data(self, data):

        j = json.loads(data)

        text = j["text"]
        date = j["created_at"]
        date = date.split()

        if 'RT' in text:
            pass

        # Checks month then date
        elif (date_collect[0] == date[1]) and (date_collect[1] == date[2]):
            fhOut.write(data)
            print(text)

        # If month to be collected is before month of tweet 
        # Or if month is the same but it's an earlier day
        elif (months[date_collect[0]] > months[date[1]]) or (date_collect[0] == date[1] and int(date_collect[1]) > int(date[2])):
            raise PastDate

        else:
            print(date, text)

        return True

    def on_error(self, status):
        print('ERROR:', status)

def main():
    try:
        l = Listener()
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        stream = Stream(auth, l)
        stream.filter(follow=['51241574'])

    except KeyboardInterrupt:
        pass

    except PastDate:
        pass

main()
fhOut.close()
