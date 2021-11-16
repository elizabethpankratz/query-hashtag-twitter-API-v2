"""
Data Collection (Fall 2021). Script 3 of 3.

If script `1_get_tweets.py` has been run again with outfiles saved in directory data2/,
then this script compares tweet IDs between initial data set (in data/) and new data set 
(in data2/) to identify which tweets have been removed from Twitter (e.g., if deleted, 
if user made their account private) and must therefore be excluded from analysis.

In:
- `data/tweets.csv`
- `data2/tweets.csv`
Out:
- `data/deleted_tweets.csv`
"""

import pandas as pd

# Read in data.
tweets1 = pd.read_csv('data/tweets.csv')
tweets2 = pd.read_csv('data2/tweets.csv')

# Get set difference between tweet IDs in first and second data sets.
not_in_2 = set(tweets1['tweet_id']) - set(tweets2['tweet_id'])

# Subset tweets1 for those tweets that were deleted.
deleted_tweets = tweets1[tweets1['tweet_id'].isin(not_in_2)]

# Save result as CSV.
deleted_tweets.to_csv('data/deleted_tweets.csv', index=False)
