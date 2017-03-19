#!/usr/bin/env python

# imports
import sys
import os
from twitter import *
import random

# get credentials
credentials = open(os.path.join(sys.path[0], 'creds.txt'))
consumer_key, consumer_secret = credentials.read()[:-1].split('\n')
credentials.close()

# authenticate app
OAUTH = os.path.join(sys.path[0], 'oauth')
if not os.path.exists(OAUTH): oauth_dance("Alt Weather Bot", consumer_key, consumer_secret, OAUTH)
token, secret = read_token_file(OAUTH)
twitter = Twitter(auth=OAuth(token, secret, consumer_key, consumer_secret))

temp = random.randrange(-350, 350)/10.0
status = "It's %s degrees outside right now" % str(temp)
twitter.statuses.update(status=status)
