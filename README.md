# ERKNews

Final Project of Intro to Computational Linguistics (LIN353C)

All code writted in Python 3

This project will take tweets from news twitter accounts as input and return
computer generated breaking news headlines as output.

Run tweet.py to generate a sentence and post it. Program will ask for
permission to post a headline before doing so.

----------------------------------------
SETUP
----------------------------------------

To use, create a Twiiter account and Twitter App at apps.twitter.com
Create comsumer key, comsumer secret, access token, and access token secret and
copy into auth.py

To change input data, change list of handles in data_collection.py

Need to install libraries TwitterSearch, Tweepy, and NLTK

If you have pip install:
$ pip install -r requirements.txt

To test installation:
$ python3
>>> import TwitterSearch, tweepy, nltk

Installation complete if this returns no errors.

----------------------------------------
HOW IT WORKS
----------------------------------------

First, a new data set is created based on the past three days worth of tweets
plus the current day from the handles list in data_collection.py

data_collection.py writes to output.txt which generate_tweet.py then intakes
and generates a sentece.

Finally, tweepy.py controls the whole process, asks if you want to post the
headline, then posts if you input 'y'

----------------------------------------
HOW TO USE
----------------------------------------

In order to post a tweet, you only need to run $ python tweet.py

**NOTE: Twitter has rules that prevent developers from streaming too much data
so if you run this program multiple times within 15 mintues, it may return an
error. Wait 15 minutes then try again.
