# Query Twitter API v2 for all tweets with a given hashtag using Python/tweepy

Scripts to:
1. Query the Twitter API v2 for all primary tweets (that is, not retweets or quote tweets) with the hashtag [#Scotstober](https://twitter.com/search?q=%23Scotstober&src=typed_query) posted in the month of October 2021.
2. Format the gathered data as a more readable HTML file (which can then be opened in a browser and exported as PDF, if desired).
3. Identify which tweets have been deleted between initial and subsequent data collection, so that these can be removed from the data set.

Directories `data/` and `data2/` contain dummy data for illustration, including free images from [placeholder.com](https://placeholder.com).

## How to use

In the terminal, set your bearer token as an environment variable (see [Twitter page on authentication](https://developer.twitter.com/en/docs/authentication/guides/authentication-best-practices)):

```
export BEARER_TOKEN='<my private token>'
```

To get all tweets that match the query defined in lines 22–23 of this script, run:

```
python 1_get_tweets.py
```

To format these tweets and their associated images as an HTML page, run:

```
python 2_html_viewer.py
```

Finally, although Twitter users don't need to give their informed consent for us to use their publicly posted data, we still need to respect their personal autonomy by excluding tweets from our analysis that have been removed from Twitter (e.g., if the original tweet was deleted, or if the user made their account private).
To identify which tweets have been removed since the initial data collection, re-run `1_get_tweets.py` with output saved this time to `data2/`, not `data/` (lines 164–165), and then run:

```
python 3_identify_deleted_tweets.py
```

## Requirements

- [Academic Research access](https://developer.twitter.com/en/products/twitter-api/academic-research) to the Twitter API.
- An existing Developer App with an associated bearer token.
- Python 3.
- Python libraries `domonic`, `datetime`, `os`, `pandas`, `pytz`, and `tweepy`.

