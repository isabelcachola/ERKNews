#################################
'''
This is the code that actually posts tweets
'''
#################################

import tweepy
from auth import TwitterAuth as TA
from generate_tweet import GenerateTweet
from data_collection import CollectData
import argparse
import nltk
import logging

def language_model(sents):
    bigrams = []
    for sent in sents:
        bigrams += list(nltk.bigrams(sent.split()))
    cpd = nltk.ConditionalProbDist(nltk.ConditionalFreqDist(bigrams), nltk.MLEProbDist)
    print(cpd)



def tweet(headline):
    auth = tweepy.OAuthHandler(TA.consumer_key, TA.consumer_secret)
    auth.set_access_token(TA.access_token, TA.access_token_secret)
    api = tweepy.API(auth)

    print('Headline:', headline)
    print()
    tweet = input('Do you want to post this headline? (y|n) ')
    api.update_status(status=headline)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate tweets')
    parser.add_argument('--data', default='output.txt', type=str)
    parser.add_argument('--n', default=100, type=int)
    parser.add_argument('--c', '--collect', action='store_true')
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

    args = parser.parse_args()

    if args.c:
        collector = CollectData(output_file=args.data)
        collector.start()

    generator = GenerateTweet(data_file=args.data)

    good_tweet = False
    while not good_tweet:
        sents = []
        for i in range(args.n):
            sent = generator.generate()
            sents.append(sent)
        best_tweet = generator.language_model(sents)
        if best_tweet is not None:
            good_tweet = True

    tweet(headline=best_tweet)
