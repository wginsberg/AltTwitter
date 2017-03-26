#!/usr/bin/env python
#
# Grab a Trump tweet from the past hour and tweet it without vowels to improve SEO

# imports
import sys
import os
from twitter import *
import datetime
import re

def seoify(s):
	return re.sub('(\S)[aeiouAEIOU]*', '\g<1>', s)

# Load the id of the last trump tweet so we know if there was a new one
if os.path.exists(os.path.join(sys.path[0], 'last_id')):
	with open(os.path.join(sys.path[0], 'last_id'), 'r') as f:
		last_id = f.read()
else:
	last_id = ''

# Get credentials
credentials = open(os.path.join(sys.path[0], 'creds.txt'))
consumer_key, consumer_secret = credentials.read()[:-1].split('\n')
credentials.close()

# Authenticate app
OAUTH = os.path.join(sys.path[0], 'oauth')
if not os.path.exists(OAUTH): oauth_dance("SEO trump", consumer_key, consumer_secret, OAUTH)
token, secret = read_token_file(OAUTH)
twitter = Twitter(auth=OAuth(token, secret, consumer_key, consumer_secret))

# Find a new trump tweet
timeline = twitter.statuses.user_timeline(screen_name="realDonaldTrump")
if timeline[0]['id'] == last_id:
	exit()

# Tweet the seo version and update last_id
twitter.statuses.update(status=seoify(timeline[0]['text']))
with open('last_id', 'w') as f:
	f.write(str(timeline[0]['id']))
