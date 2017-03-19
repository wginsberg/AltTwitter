# imports
import os 
from twitter import *
import random

# get credentials
credentials = open('creds.txt')
consumer_key, consumer_secret = credentials.read()[:-1].split('\n')
credentials.close()

print consumer_key
print consumer_secret

# authenticate app
OAUTH = './oauth'
if not os.path.exists(OAUTH): oauth_dance("Alt Weather Bot", consumer_key, consumer_secret, OAUTH)
token, secret = read_token_file(OAUTH)
twitter = Twitter(auth=OAuth(token, secret, consumer_key, consumer_secret))

temp = random.randrange(-350, 350)/10.0
status = "It's %s degrees outside right now" % str(temp)

twitter.statuses.update(status=status)
