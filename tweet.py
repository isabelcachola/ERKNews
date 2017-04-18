#################################
'''
This is the code that actually posts tweets
'''
#################################

def main():

    import tweepy
    from auth import TwitterAuth as TA
    import generate_tweet

    auth = tweepy.OAuthHandler(TA.consumer_key, TA.consumer_secret)
    auth.set_access_token(TA.access_token, TA.access_token_secret)
    api = tweepy.API(auth)

    headline = generate_tweet.generate()

    api.update_status(status=headline)
    print(headline)

main()
