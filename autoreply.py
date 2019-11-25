#!/usr/bin/env python
# tweepy-bots/bots/autoreply.py

import tweepy
import logging

import time

from credentials import *  # use this one for testing

# use this for production; set vars in heroku dashboard
#from os import environ
#CONSUMER_KEY = environ['CONSUMER_KEY']
#CONSUMER_SECRET = environ['CONSUMER_SECRET']
#ACCESS_KEY = environ['ACCESS_KEY']
#ACCESS_SECRET = environ['ACCESS_SECRET']


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
            logger.info(f"Answering to {tweet.user.name}")

            if not tweet.user.following:
                tweet.user.follow()

            api.update_status(
                status="Hullooooooo @" + str(tweet.user.name),
                in_reply_to_status_id=tweet.id,
            )
    return new_since_id

def main():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    since_id = 1
    while True:
        since_id = check_mentions(api, ["hello", "shut up", "hullo", "hi", "hiya"], since_id)
        logger.info("Waiting...")
        time.sleep(60)

if __name__ == "__main__":
    main()