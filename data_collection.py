#####################################
'''
This code parses through a list of handles, streams their timeline for the past
4 days, then writes to an output file (output.txt) which generate_tweet.py then
takes as input to generate sentences.
Retweets and links are excluded.
'''
#####################################

from TwitterSearch import *
from auth import TwitterAuth

class PastDate(Exception):
    pass

def main():
    from datetime import datetime, timedelta
    import time
    import progressbar

    handles = ['@BBCWorld', '@cnnbrk', '@reuters', '@AP']

    output = open('output.txt', 'w')

    print('Starting data collection. Please hold...')

    count = 0
    bar = progressbar.ProgressBar(max_value=4)

    # Creates list of dates to collect
    dates = []
    for i in range(4):
        date_collect_orig = datetime.now() - timedelta(days=(i))
        date_collect_orig = date_collect_orig.strftime("%m %d %Y")
        date_collect = date_collect_orig.split()
        date_collect = list(map(int, date_collect))
        dates.append(date_collect)
    print()

    # Hard code months
    months = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}

    days_collected = 0
    # For each of the past 4 days
    for date_collect in dates:
        # For all the handles you want to collect
        for handle in handles:

            try:
                # Create a Twitter search object
                ts = TwitterSearch(
                    consumer_key = TwitterAuth.consumer_key,
                    consumer_secret = TwitterAuth.consumer_secret,
                    access_token = TwitterAuth.access_token,
                    access_token_secret = TwitterAuth.access_token_secret
                    )

                tuo = TwitterUserOrder(handle) # Twitter User Order


                # Parses through timeline and collects tweets until it is past
                # the date of collection
                for tweet in ts.search_tweets_iterable(tuo):
                    text = tweet['text']
                    date = tweet['created_at']
                    date = date.split()

                    if 'RT' in tweet['text']:
                        pass
                    elif len(tweet['text'].split()) < 4:
                        pass

                    # Checks month then date
                    elif (date_collect[0] == months[date[1]]) and (date_collect[1] ==
                    int(date[2])):
                        if 'http' in tweet['text']:
                            idx = tweet['text'].index('http')
                            tweet['text'] = tweet['text'][:idx]
                        if '\n' in tweet['text']:
                            tweet['text'] = tweet['text'].replace('\n','')
                        output.write(tweet['text'] + '\n')
                        count += 1
                        #print('@%s tweeted: %s' %(tweet['user']['screen_name'], tweet['text']))

                    # If month to be collected is before month of tweet
                    # Or if month is the same but it's an earlier day
                    elif ((date_collect[0]) > months[date[1]]) or (date_collect[0]
                    == months[date[1]] and (date_collect[1]) > int(date[2])):
                        raise PastDate

                    else:
                        pass

            except TwitterSearchException as e:
                print(e)

            except PastDate:
                pass
                #print()

            except KeyboardInterrupt:
                print()
                print('Keyboard Interrupt. Collection stopped.')
        days_collected += 1 
        bar.update(days_collected)

    bar.finish()
    output.close()
    print()
    print()
    print('Collection complete.')
    print('Number of tweets collected:', count)
    print()

main()
