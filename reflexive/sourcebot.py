# imports
import os 
from twitter import *

# get credentials
credentials = open('creds.txt')
consumer_key, consumer_secret = credentials.read()[:-1].split('\n')
credentials.close()

# authenticate app
OAUTH = './oauth'
if not os.path.exists(OAUTH): oauth_dance("SourceBot", consumer_key, consumer_secret, OAUTH)
token, secret = read_token_file(OAUTH)
twitter = Twitter(auth=OAuth(token, secret, consumer_key, consumer_secret))

# tweet this source code
f = open('sourcebot.py')
map((lambda line: twitter.statuses.update(status=line)), filter((lambda line: line != '\n'), f))
f.close()
