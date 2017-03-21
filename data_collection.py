from TwitterSearch import *
from auth import TwitterAuth
import json

class PastDate(Exception):
    pass

def main():
    #output = open('output.json', 'w')
    output = open('output.txt', 'w')
    handle = input('Enter handle to collect (@AP): ')
    date_collect_orig = input("Enter date to collect (Mar 18 2017): ")
    date_collect = date_collect_orig.split()

    # Hard code months
    months = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}

    try:
        tuo = TwitterUserOrder(handle) # Twitter User Order

        # Create a Twitter search object
        ts = TwitterSearch(
            consumer_key = TwitterAuth.consumer_key,
            consumer_secret = TwitterAuth.consumer_secret,
            access_token = TwitterAuth.access_token,
            access_token_secret = TwitterAuth.access_token_secret
        )

        output.write('Handle collected: ' + handle + '\n')
        output.write('Date collected: ' + date_collect_orig + '\n' )

        for tweet in ts.search_tweets_iterable(tuo):
            text = tweet['text']
            date = tweet['created_at']
            date = date.split()

            if 'RT' in tweet['text']:
                pass

            # Checks month then date
            elif (date_collect[0] == date[1]) and (date_collect[1] == date[2]):
                #j = json.dumps(tweet)
                #output.write(j)
                output.write(tweet['text'] + '\n')
                print('@%s tweeted: %s' %(tweet['user']['screen_name'], tweet['text']))

            # If month to be collected is before month of tweet 
            # Or if month is the same but it's an earlier day
            elif (months[date_collect[0]] > months[date[1]]) or (date_collect[0] == date[1] and int(date_collect[1]) > int(date[2])):
                raise PastDate

            else:
                pass 

    except TwitterSearchException as e:
        print(e)

    except PastDate:
        print()
        print('Collection complete for %s.' %(date_collect_orig))

    except KeyboardInterrupt:
        print()
        print('Keyboard Interrupt. Collection stopped.')

    output.close()
main()
