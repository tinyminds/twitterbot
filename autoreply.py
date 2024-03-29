#!/usr/bin/env python
# tweepy-bots/bots/autoreply.py

import tweepy
import logging
import time
import sys
import os

from generate_advertisement import get_ad
#from credentials import *  # use this one for testing

# use this for production; set vars in heroku dashboard

CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')
ACCESS_KEY = os.environ.get('ACCESS_KEY')
ACCESS_SECRET = os.environ.get('ACCESS_SECRET')
SINCE_ID = os.environ.get('SINCE_ID')

INTERVAL = 60 * 60 * 6  # tweet every 6 hours
#INTERVAL = 15  # every 15 seconds, for testing
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def check_mentions(api, keywords, since_id):
    logger.info("Retrieving mentions")
    new_since_id = since_id
    for tweet in tweepy.Cursor(api.mentions_timeline,
        since_id=since_id).items():
        new_since_id = max(tweet.id, new_since_id)
        if tweet.in_reply_to_status_id is not None:
            continue
        if any(keyword in tweet.text.lower() for keyword in keywords):
            logger.info(f"Answering to {tweet.user.screen_name} - {new_since_id}")

            if not tweet.user.following:
                tweet.user.follow()

            api.update_status(
                status="Hullo there @" + str(tweet.user.screen_name) + " " + str(get_ad()),
                in_reply_to_status_id=tweet.id,
            )
    return new_since_id

def main():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    since_id = SINCE_ID #reset env variable with last id if it crashes. find a better way. date?
    logger.info(since_id)
    while True:
        since_id = check_mentions(api, ["hello", "shut up", "hullo", "hi", "hiya", "yo", "morning"], since_id)
        logger.info("Waiting...")
        logger.info(since_id)
        time.sleep(300)
if __name__ == "__main__":
    main()