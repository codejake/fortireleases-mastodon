# Fortireleases Mastodon Bot

This code checks the Fortinet Firmware Updates RSS feed, looks for new entries, and posts a tweet for each at https://hacyderm.io/@fortireleases

Take this more-or-less current source and make your own Twitter bot, or do what you want with it. I did not invest a lot of time in this, sorry.

You'll need your own API keys from https://developer.twitter.com

## Rough install process

1. Get your own API keys from https://developer.twitter.com

2. `git clone` this repo.

3. `cp config.py.sample config.py` and add your API keys.

4. Run `python3 -m venv venv && source venv/bin/activate` or whatever.

5. Run `pip install -r requirements.txt`

6. Edit `main.py` to your tastes, and run `python3 ./main.py`.

7. If you're using this code for similar purposes, you can call run.sh via crontab or systemd.
