"""
Data Collection (Fall 2021). Script 2 of 3.

Formats tweet data (output from `1_get_tweets.py`) as HTML page for readability.

In:
- `data/tweets.csv`
- `data/media.csv`
Out:
- `data/viewer.html`
"""

from datetime import datetime
from domonic.html import *
import pandas as pd

# Read in data, order chronologically.
tweets = pd.read_csv('data/tweets.csv')
media = pd.read_csv('data/media.csv')
tweets = tweets.sort_values(by='created_at').reset_index(drop=True)

# Create list that will collect divs for each tweet in the for loop below.
tweet_divs = []

# Set current date to before October begins.
curr_date = "2021-09-30"

# Go row by row through the dataset, formatting each tweet as a <div />.
for idx, row in tweets.iterrows():
    
    # Grab date and time from the string in 'created_at'.
    date = row['created_at'].split('T')[0]
    time = row['created_at'].split('T')[1][:5]
    
    # If the date is different from curr_date, save it as the new curr_date
    # and prep a header element to be added to this tweet's div.
    if date != curr_date:
        curr_date = date
        date_head = h1(date, hr())
    else:
        date_head = ''
    
    # Grab media, if the tweet has any.
    if row['has_media']:
        
        # The content in column 'url' is only a valid URL if the media type is a photo.
        # If it's a video or an animated gif, this cell will be empty. But the resulting
        # <img /> tag will just have src = "nan" and display empty, so it's not a problem.
        media_urls = list(media.loc[media['tweet_id'] == row['tweet_id'], 'url'])
        media_tags = [img(_src = url, _width='400') for url in media_urls]
    else:
        media_tags = ['']
    
    # Get data from current row for current tweet, save as div, and add to list.
    tweet = div(
        date_head,
        p(b(row['name']), ' @{0}'.format(row['username']), i(' ({0})'.format(row['description']))),
        p(row['text'].replace('\n', '<br>')),
        p(i('Replies: {0} - Quotes: {1} - Retweets: {2} - Likes: {3}'.format(row['reply_count'], row['quote_count'], row['retweet_count'], row['like_count']))),
        p(i(date, ' at ', time)),
        *media_tags,
        hr())
    tweet_divs.append(tweet)

# Unpack all these divs and save as elements in the page body.
bod = body(*tweet_divs)

# Get final string set up (specify page width, char encoding).
page = '<style> body{max-width: 400px; margin: auto} </style>' + '<meta charset="UTF-8">\n' + f"{bod}"

# Save string as html file.
with open("data/viewer.html", "w", encoding='utf-8') as file:
    file.write(page)
