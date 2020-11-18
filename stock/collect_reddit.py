import praw
import yaml

with open("reddit_keys.yaml", 'r') as stream:
    USER_PARAMETERS = yaml.safe_load(stream)

LIMIT = 200

items = ["title", "score", "id", "url", "num_comments", "created"]


class RedditPipeline(object):
    def __init__(self, subreddit):
        praw_connection = praw.Reddit(**USER_PARAMETERS)
        self.subreddit = praw_connection.subreddit(subreddit)

    def get_posts(self):
        return list({item: submission.__getattribute__(item) for item in items}
                    for submission in self.subreddit.hot(limit=LIMIT))
