import yfinance as yf
import pandas as pd


def create_finance_dataframe(tickers, start, end, interval, price):
    fi_df = yf.download(
        tickers=tickers,
        start=start, end=end,
        interval=interval)
    fi_df = fi_df[price]
    return fi_df


def features_creation_lags(df, id_col, date_col, target, lag_days):
    df_copy = df.copy().sort_values([id_col, date_col])
    df_copy = df_copy.assign(**{
        '{}_lag_{}'.format(col, lag_d): df_copy.groupby(id_col)[col]
        .transform(lambda x: x.shift(lag_d))
        for lag_d in lag_days for col in target})
    return df_copy.drop(columns=target)


def features_creation_rollings(df, id_col, date_col, target, windows, lag, func=None):
    if func is None:
        func = ['mean']
    df_copy = df.copy().sort_values([id_col, date_col])
    df_copy = df_copy.assign(**{
        'rolling_{}_{}'.format(f, w): df_copy.groupby(id_col)[col]
        .transform(lambda x: x.shift(lag).rolling(w).agg(f))
        for w in windows for f in func for col in target})
    return df_copy.drop(columns=target)


def features_creation_rollings_with_sliding(df, id_col, date_col, target, windows, shifts, func=None):
    df_copy = df.copy().sort_values([id_col, date_col])
    df_copy = df_copy.assign(**{
        'rolling_{}_{}_{}'.format(f, w, s): df_copy.groupby(id_col)[col]
        .transform(lambda x: x.shift(s).rolling(w).agg(f))
        for s in shifts for w in windows for f in func for col in target})
    return df_copy.drop(columns=target)


def features_creation_date_extract_components(df, id_col, date_col):
    df_copy = df[[date_col]+[id_col]].copy()
    date_cols = ['month', 'dayofyear', 'quarter', 'dayofweek', 'days_in_month', 'weekofyear', 'year']
    df_copy[date_cols] = df_copy[date_col].apply(lambda x:
                             {'month': x.month, 'dayofyear': x.dayofyear,
                              'quarter': x.quarter, 'dayofweek': x.dayofweek,
                              'days_in_month': x.days_in_month, 'weekofyear': x.weekofyear,
                              'year': x.year}).apply(pd.Series)
    df_copy['day_since_begin'] = (df_copy[date_col] - df_copy[date_col].min()).apply(lambda x: x.days)
    return df_copy
