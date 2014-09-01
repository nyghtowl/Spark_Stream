"""
Trying out streaming data from Twitter

Code example pulled from :
https://www.wakari.io/sharing/bundle/wakari_demo/realtime_twitter_analysis 
"""

import os
import twitter
import json
from dateutil.parser import parse

from nltk.corpus import stopwords
from nltk import wordpunct_tokenize
import numpy as np

TWITTERKEY = os.environ['TWITTERKEY']
TWITTERSEC = os.environ['TWITTERSEC']
TWITTERTOKEN = os.environ['TWITTERTOKEN']
TWITTERACCESS = os.environ['TWITTERACCESS']


class Tweet(dict):
    def __init__(self, raw_tweet):
        super(Tweet, self).__init__(self)
        if raw_tweet and 'delete' not in raw_tweet:
            self['timestamp'] = parse(raw_tweet[u'created_at']
                                ).replace(tzinfo=None).isoformat()
            self['text'] = raw_tweet['text']
            self['hashtags'] = [x['text'] for x in raw_tweet['entities']['hashtags']]
            self['geo'] = raw_tweet['geo']['coordinates'] if raw_tweet['geo'] else None
            self['id'] = raw_tweet['id']
            self['screen_name'] = raw_tweet['user']['screen_name']
            self['user_id'] = raw_tweet['user']['id'] 


def twitter_conn():
    twitter_stream = twitter.TwitterStream(auth=twitter.OAuth(
            token=TWITTERTOKEN,
            token_secret=TWITTERACCESS,
            consumer_key=TWITTERKEY,
            consumer_secret=TWITTERSEC))
    stream = twitter_stream.statuses.sample(block=True)
    
    testing = stream.next() # This is just to make sure the stream is emitting data.

    print testing
    return stream

def convert_stream(raw_data):
    print json.dumps(raw_data, indent=2, sort_keys=True)

def get_likely_language(input_text):
    input_text = input_text.lower()
    input_words = wordpunct_tokenize(input_text)
    
    likely_language = 'unknown'
    likely_language_matches = 0
    total_matches = 0
    stopword_sets = dict([(lang, set(stopwords.words(lang))) for lang in stopwords._fileids])
    
    for language in np.random.permutation(stopwords._fileids):
        language_matches = len(set(input_words) & stopword_sets[language])
        total_matches += language_matches
        if language_matches > likely_language_matches:
            likely_language_matches = language_matches
            likely_language = language
            
    return (likely_language, likely_language_matches, total_matches)


def main():
    stream = twitter_conn()
    T = None
    while not T or 'delete' in raw_T:
        T = Tweet(stream.next())

    for i in range(5):
        T = Tweet(stream.next())
        if T:
            T['language'] = get_likely_language(T['text'])[0]
            print "%s, %i, %i: %s" % (get_likely_language(T['text']) + (T['text'],))