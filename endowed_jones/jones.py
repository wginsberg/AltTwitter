#!/usr/bin/env python

# imports
from twitter import *
import os
import sys
import re

# Get credentials
credentials = open(os.path.join(sys.path[0], 'creds.txt'))
consumer_key, consumer_secret = credentials.read()[:-1].split('\n')
credentials.close()

# Authenticate app
OAUTH = os.path.join(sys.path[0], 'oauth')
if not os.path.exists(OAUTH): oauth_dance("SEO trump", consumer_key, consumer_secret, OAUTH)
token, secret = read_token_file(OAUTH)
twitter = Twitter(auth=OAuth(token, secret, consumer_key, consumer_secret))

timeline = twitter.statuses.user_timeline(screen_name="DowJones", include_rts=False)

#idk just take the first one how about?
text = timeline[0]['text']
first_phrase = re.split('[\.\?\!\:]', text)[0]
status = '%s if you know what I mean ;)' % first_phrase

twitter.statuses.update(status=status)
