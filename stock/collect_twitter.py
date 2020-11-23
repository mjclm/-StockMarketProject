import requests

import yaml

# Buildings queries
# Boolean syntax to group multiple operators
# (Standalone operators not recommended)

# Successive operators with a space btw them means "AND" logic.
# Ex: snow day #NoSchool -> Tweets with all the keywords

# Successive operators with a OR btw them means "OR" logic.
# Ex: grumpy OR cat OR #meme -> Tweets with any of the keywords

# Use parentheses to group operators together
# use a dash to negate a keyword or operators grouped with parentheses.

# Note:
# queries max length: 512
# All operators can be negated
# Recommended to negate each individual operator instead to
# negate a set of operators grouped together.

# use bearer token


def create_twitter_url():
    # url-encoding
    # TODO: Add a context to the tweets
    # health situation, promotion period, pollution, fraud, new product
    # new discovery, strike, 
    handle = requests.utils.quote(
        "(lang:en OR lang:fr OR lang:de OR lang:es) " # Language of tweets
        "(#Facebook OR #Amazon OR #Microsoft OR #Google OR #Apple) " # List of brand citation
        "is:verified" # Only account verified
    )
    max_results = 10
    fields = ['id', 'text', 'created_at']
    mrf = "max_results={}".format(max_results)
    tf = "tweet.fields={}".format(",".join(fields))
    # start_time = "start_time={}".format("2020-11-15T01:00:00-05:00")
    # end_time = "end_time={}".format("2020-11-16T01:00:00-05:00")
    q = "query={}".format(handle)
    url = "https://api.twitter.com/2/tweets/search/recent?{}&{}&{}".format(
        # start_time, end_time,
        mrf, tf, q
    )
    return url


def process_yaml():
    with open("twitter_keys.yaml") as file:
        return yaml.safe_load(file)


def create_bearer_token(data):
    return data["bearer_token"]


def twitter_auth_and_connect(bearer_token, url):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    response = requests.request("GET", url, headers=headers)
    return response.json()


def give_tweets():
    url = create_twitter_url()
    data = process_yaml()
    bearer_token = create_bearer_token(data)
    return twitter_auth_and_connect(bearer_token, url)
