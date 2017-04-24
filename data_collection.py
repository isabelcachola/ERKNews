#####################################
'''
This code takes twitter handles and dates as input and outputs a text file
(output.txt) which must then be converted to csv using data2spreadsheet.py
Retweets and links are excluded.
'''
#####################################

from TwitterSearch import *
from auth import TwitterAuth
import json
import csv

class PastDate(Exception):
    pass

def main():
    from datetime import datetime, timedelta

    handles = ['@BBCWorld', '@cnnbrk', '@reuters', '@AP']

    output = open('output.txt', 'w')
    dates = []
    for i in range(3):
        date_collect_orig = datetime.now() - timedelta(days=(i+1))
        date_collect_orig = date_collect_orig.strftime("%m %d %Y")
        date_collect = date_collect_orig.split()
        date_collect = list(map(int, date_collect))
        dates.append(date_collect)
    print()

    # Hard code months
    months = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}
    for date_collect in dates:
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
                        #output += tweet['text'] + '\n'
                        output.write(tweet['text'] + '\n')
                        print('@%s tweeted: %s' %(tweet['user']['screen_name'], tweet['text']))

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
                print()
                #print('Collection complete for %s.' %(date_collect_orig))

            except KeyboardInterrupt:
                print()
                print('Keyboard Interrupt. Collection stopped.')

    output.close()
    print('Collection complete for %s.' %(date_collect_orig))

    #d2s.convert(output)
main()
