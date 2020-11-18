# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
# https://github.com/alan-turing-institute/sktime

# automatic FE: https://www.featuretools.com/, autofeat, gplearn
# auto FS: SelectFromModel (sklearn), Recursive Feature Elimination, Pearson correlation
# SelectKBest (Chi-2), VarianceThreshold,
# Explaining: ELI5, LIME, SHAP

# See other tips:
# https://www.kaggle.com/vbmokin/data-science-for-tabular-data-advanced-techniques
# https://www.kaggle.com/youhanlee/simple-quant-features-using-python


from stock.pipelines import MongoDBPipeline
from stock.collect_reddit import RedditPipeline

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    REDDIT_NEWS_LINK = "https://www.reddit.com/r/worldnews/"
    TICKERS = ["GOOG", "AMZN", "FB", "AAPL", "MSFT"]
    START = "2019-01-01"
    END = "2020-10-20"
    INTERVAL = "1d"
    PRICE = "Close"
    DATASET_FINANCE_PARAMS = dict(
        (("tickers", TICKERS), ("start", START), ("end", END),
         ("interval", INTERVAL), ("price", PRICE))
    )

    # Preview of data
    # gafam_close_df = create_finance_dataframe(**DATASET_FINANCE_PARAMS)

    # Unpivot the dataframe
    # stacked_df = (gafam_close_df.stack().reset_index().rename(columns={'level_1': 'Symb', 0: PRICE}))

    # Reddit

    # Export the reddit post into the Mongo DB
    SUBREDDIT = 'worldnews'
    mongo_pipe = MongoDBPipeline()
    reddit_pipe = RedditPipeline(SUBREDDIT)
    posts = reddit_pipe.get_posts()
    mongo_pipe.process_item(posts)
