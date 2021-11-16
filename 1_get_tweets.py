"""
Data Collection (Fall 2021). Script 1 of 3.

Queries Twitter for all primary tweets containing #scotstober posted in October 2021.
Requires academic research track access to Twitter API v2.

In:
- Environment variable BEARER_TOKEN for authenticating access to API
  (set in shell using `export BEARER_TOKEN='<my private token>'` before running this script)
Out:
- `data/tweets.csv`
- `data/media.csv`
"""

from datetime import datetime
import pandas as pd
import tweepy
import pytz
import os

# We want tweets containing HASHTAG that aren't retweets or quote tweets.
HASHTAG      = '#scotstober'
QUERY        = HASHTAG + ' -is:retweet -is:quote'

# We want tweets posted between October 1 at 00:00 and November 1 at 00:00.
STARTDATE    = datetime(2021,10,1,0,0,0,0,pytz.UTC)
ENDDATE      = datetime(2021,11,1,0,0,0,0,pytz.UTC)

# Get authentication information from the shell environment.
bearer_token = os.environ.get('BEARER_TOKEN')

# If environment variable isn't defined, a reminder pops up.
assert bearer_token != None, "Remember to set API credentials as environment variables first!"

# Create .Client() object that will let us access the full archive.
client = tweepy.Client(bearer_token = bearer_token,
                       return_type=dict)

# Get the tweets. They can't be queried all at once, so we have to go page by (virtual) page.
# Repeating all this code is pretty ugly, but if I try to write this more efficiently
# (with a while loop, with tweepy.Paginator()... ), I exceed the API's rate limit :(
# So this is what we get.
tweets = client.search_all_tweets(query=QUERY, 
                                  tweet_fields=['created_at', 'entities', 'public_metrics'],
                                  media_fields=['url'],
                                  user_fields=['description'],
                                  expansions=['attachments.media_keys', 'author_id'],
                                  start_time = STARTDATE,
                                  end_time = ENDDATE,
                                  max_results = 500)

tweets2 = client.search_all_tweets(query=QUERY, 
                                  tweet_fields=['created_at', 'entities', 'public_metrics'],
                                  media_fields=['url'],
                                  user_fields=['description'],
                                  expansions=['attachments.media_keys', 'author_id'],
                                  start_time = STARTDATE,
                                  end_time = ENDDATE,
                                  max_results = 500,
                                  next_token = tweets['meta']['next_token'])

tweets3 = client.search_all_tweets(query=QUERY, 
                                  tweet_fields=['created_at', 'entities', 'public_metrics'],
                                  media_fields=['url'],
                                  user_fields=['description'],
                                  expansions=['attachments.media_keys', 'author_id'],
                                  start_time = STARTDATE,
                                  end_time = ENDDATE,
                                  max_results = 500,
                                  next_token = tweets2['meta']['next_token'])

tweets4 = client.search_all_tweets(query=QUERY, 
                                  tweet_fields=['created_at', 'entities', 'public_metrics'],
                                  media_fields=['url'],
                                  user_fields=['description'],
                                  expansions=['attachments.media_keys', 'author_id'],
                                  start_time = STARTDATE,
                                  end_time = ENDDATE,
                                  max_results = 500,
                                  next_token = tweets3['meta']['next_token'])

# Check if there are more pages of tweets that need retrieving; if we've seen everything,
# there'll be no attribute 'next_token' under 'meta', triggering the except block.
try:
    tweets4['meta']['next_token']
    print('There are more pages')
except:
    print('No more pages')

# Combine pages into a list that we will iterate through below.
all_pages = [tweets, tweets2, tweets3, tweets4]

# Create list that will collect the dfs for each page; will each be concatenated at the end
# into a master df.
page_tweet_dfs = []
page_media_dfs = []

for page in all_pages:

    # Make df with media information. Include extra column so that tweet IDs can be added.
    media_df = pd.DataFrame(page['includes']['media'])
    media_df['tweet_id'] = None

    # Construct basis of df using information in tweets['data'].
    tweet_data_list = []

    for item in page['data']:

        tweet_data = {
            'tweet_id': item['id'],
            'author_id': item['author_id'],
            'text': item['text'],
            'hashtags': [tag['tag'] for tag in item['entities']['hashtags']],
            'created_at': item['created_at'],
            'mined_at': datetime.now(),
            'like_count': item['public_metrics']['like_count'],
            'quote_count': item['public_metrics']['quote_count'],
            'reply_count': item['public_metrics']['reply_count'],
            'retweet_count': item['public_metrics']['retweet_count'],
        }

        tweet_data_list.append(tweet_data)

        # Flag whether the tweet has any media attached; if yes, item['attachments'] exists, if not, it doesn't.
        try:
            media_keys = item['attachments']['media_keys']
            media_bool = 1

            # Add tweet ID to media_df.
            for key in list(media_keys): # in case a singleton element isn't a list by default
                media_df.loc[media_df.media_key == key, 'tweet_id'] = item['id']
        except:
            media_bool = 0

        tweet_data['has_media'] = media_bool

    # Convert this list of dictionaries into a dataframe and add to page_tweet_dfs.
    tweets_df = pd.DataFrame(tweet_data_list)
    page_tweet_dfs.append(tweets_df)
    
    # Add media df to page_media_dfs.
    page_media_dfs.append(media_df)

# Concatenate lists of dfs to single, large df.
all_pages_tweets_df = pd.concat(page_tweet_dfs)
all_pages_media_df = pd.concat(page_media_dfs)
all_pages_media_df = all_pages_media_df.reset_index(drop=True)

# Same thing for users; go through pages, grab info.
page_user_dfs = []

for page in all_pages:
    # Make df with user information and add to list.
    users_df = pd.DataFrame(page['includes']['users'])
    users_df = users_df.rename(columns={'id':'author_id'})
    page_user_dfs.append(users_df)

# Concatenate pages into a single df, drop duplicated rows, and merge with all_pages_tweets_df.
all_pages_users_df = pd.concat(page_user_dfs)
all_pages_users_df.drop_duplicates(inplace=True)
all_pages_tweets_df = all_pages_users_df.merge(all_pages_tweets_df, on='author_id')

# Save dfs to data/.
all_pages_tweets_df.to_csv('data/tweets.csv', index=False)
all_pages_media_df.to_csv('data/media.csv')

