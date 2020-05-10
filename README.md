# Reddit-Telltale-Vote-Counter

## Setup

This script requires [Python 3](https://www.python.org/downloads/) and [PRAW](https://praw.readthedocs.io/en/latest/getting_started/installation.html).

Further you need to create a config.ini file, in the format of config_example.ini, containing the login information for a Reddit-Bot so the script can interact with Reddit.  
You can simply generate that in your Reddit-Account under Preferences/Apps or by following this guide: https://www.pythonforengineers.com/build-a-reddit-bot-part-1/

The URL and choices are already entered in the script, you can see them at the top of voteCounter.py.

## Use

Afterwards just run the script from commandline using
```
Python voteCounter.py
```
or depending on your system
```
python3 voteCounter.py
```

## How it works
The script runs chronolgically through the comments of the specified thread, newest to oldest.  
For each comment it checks that the author has not yet voted, that his Reddit account is at least 3 days younger than the comment and that the comment was made within 48 hours of the threads creation.  
Then it checks for each pairing whether none, one or both of the characters are mentioned in the comment (order and case are irrelevant).
If none or both are found, no votes are recorded, only if exactly one is found, that choices vote count is increased.
