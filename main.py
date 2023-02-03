#!/usr/bin/env python3

import feedparser
import mastodon
import re
import sys
import config as cfg

from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from mastodon import Mastodon

# Fortinet RSS feed to parse.
feed = 'https://pub.kb.fortinet.com/rss/firmware.xml'

# For RSS entry filtering
past_hour = datetime.now() - timedelta(hours = 1)
past_week = datetime.now() - timedelta(days = 7)
past_month = datetime.now() - timedelta(days = 30)

d = feedparser.parse(feed)

# Do the Mastodon.
m = Mastodon(access_token = cfg.mastodon['access_token'], api_base_url = cfg.mastodon['instance'])

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
        toot_text = f"Posted: {mo.group(1)}\n\n{entry.published}\n\n{entry.link}\n\n#fortinet"
        #api.update_status(tweet_text)
        m.toot(toot_text)
        print(toot_text)

if counter == 0:
    print("No new entries found.")



print(cfg.mastodon['instance'])