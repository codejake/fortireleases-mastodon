#!/usr/bin/env python3

import feedparser
import re
import sys
import tweepy
import config as cfg

from bs4 import BeautifulSoup
from datetime import datetime, timedelta

# Fortinet RSS feed to parse.
feed = 'https://pub.kb.fortinet.com/rss/firmware.xml'

# For RSS entry filtering
past_hour = datetime.now() - timedelta(hours = 1)
past_week = datetime.now() - timedelta(days = 7)
past_month = datetime.now() - timedelta(days = 30)

# Authenticate to Twitter
auth = tweepy.OAuthHandler(cfg.twitter["consumer_key"], cfg.twitter["consumer_secret"])
auth.set_access_token(cfg.twitter["access_token"], cfg.twitter["access_token_secret"])
api = tweepy.API(auth)

d = feedparser.parse(feed)

# Count how many new entries.
counter = 0

for entry in d.entries:
    soup = BeautifulSoup(entry.description, 'html.parser')

    pattern = re.compile(r'^(.*?) and release notes')
    mo = pattern.search(soup.p.text)

    published_dt = datetime(*entry.published_parsed[:6], tzinfo=None)

    if not mo:
        # Perhaps in the future, put a slack webhook notification in here, instead.
        print("[!] Could not find any valid entries in the RSS feed!")
        sys.exit()

    # If entry date is newer than an hour... (prod = <, debug = >)
    if past_hour < published_dt:
        counter += 1 # Update counter
        tweet_text = f"Posted: {mo.group(1)}\n\n{entry.published}\n\n{entry.link}"
        #api.update_status(tweet_text)
        print(tweet_text)

# if counter == 0:
#     print("[*] No new posts found.")
# else:
#     print(f"[*] {counter} new posts found.")
