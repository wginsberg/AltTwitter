#!/usr/bin/env python

# imports
from twitter import *
import os
import sys
import random # funny idea - don't even do it randomly each time
import re

# Construct a dictionary to translate between teams
def setup_translation():
		
	with open("names.csv") as f:
		vocabulary = [line.split(",") for line in f.read().split("\n")[1:]]

	# In the absence of a nickname, just use the team name
	for i in range(len(vocabulary)):
		if not vocabulary[i][2]:
			vocabulary[i][2] = vocabulary[i][1] 

	offset = random.randint(1, len(vocabulary))
	size = len(vocabulary)

	translation = {}
	for i in range(len(vocabulary)):
		for j in range(len(vocabulary[i])):
			translation[vocabulary[i][j]] = vocabulary[(i + offset) % size][j]

	return vocabulary, translation


def translate(status, translation):

	# Translate every team specific word in the vocabulary
	for word in list(set([word for team in vocabulary for word in team])):
		status = re.sub(word, translation[word], status, re.IGNORECASE)

	return status


def choose_tweets(api_response, n=1):
	"""
	>>> api_response = {'statuses' : [{'text': 'A good tweet'}, {'text': 'A bad tweet https://t.co/'}]}
	>>> choose_tweets(api_response)
	[{'text': 'A good tweet'}]
	"""

	tco_pattern = re.compile('t\.co')

	# I want to FP so hard
	filtered = []
	for tweet in api_response['statuses']:
		if not re.search(tco_pattern, tweet['text']):
			filtered.append(tweet)

	return filtered[:n]

def main(vocabulary, translation):

	# Get credentials
	credentials = open(os.path.join(sys.path[0], 'creds.txt'))
	consumer_key, consumer_secret = credentials.read()[:-1].split('\n')
	credentials.close()

	# Authenticate app
	OAUTH = os.path.join(sys.path[0], 'oauth')
	if not os.path.exists(OAUTH): oauth_dance("SEO trump", consumer_key, consumer_secret, OAUTH)
	token, secret = read_token_file(OAUTH)
	twitter = Twitter(auth=OAuth(token, secret, consumer_key, consumer_secret))

	# Search for tweets about a random team
	team_i = random.randint(0, len(vocabulary) - 1)
	search_for = '%s %s' % (vocabulary[team_i][0], vocabulary[team_i][1])
	
	print 'Searching for tweets about "%s"' % search_for

	response = twitter.search.tweets(q=search_for, lang='en', result_type="popular")

	print 'Found %s tweets' % len(response['statuses'])

	filtered = choose_tweets(response, 50)

	print 'Filtered down to %s tweets' % len(filtered)

	twitter.statuses.update(status=translate(filtered[0]['text'], translation))

if __name__ == "__main__":

	vocabulary, translation = setup_translation()
	main(vocabulary, translation)






