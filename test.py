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

fhOut =  open('output.json', 'a')

class Listener(StreamListener):
    def on_data(self, data):
        fhOut.write(data)

        j = json.loads(data)

        text = j["text"]
        print(text)

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

main()
fhOut.close()
