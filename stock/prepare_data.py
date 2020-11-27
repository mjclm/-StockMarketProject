import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd


def create_finance_dataframe(tickers, start, end, interval, price):
    fi_df = yf.download(
        tickers=tickers,
        start=start, end=end,
        interval=interval)
    fi_df = fi_df[price]
    return fi_df


def normalize_dataframe(df, cols='All'):
    if cols == 'All':
        cols = df.columns
    df[cols] = (df[cols] - df[cols].mean()) / df[cols].std()
    return df


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


def features_creation_date_extract_components(df, date_col):
    df_copy = df.copy()
    df_copy[['month', 'dayofyear', 'quarter', 'dayofweek', 'days_in_month', 'weekofyear', 'year']] = df_copy[date_col].apply(lambda x:
                      {'month': x.month, 'dayofyear': x.dayofyear,
                       'quarter': x.quarter, 'dayofweek': x.dayofweek,
                       'days_in_month': x.days_in_month, 'weekofyear': x.weekofyear,
                       'year': x.year}).apply(pd.Series)
    df_copy['day_since_begin'] = (df_copy.Date - df_copy.Date.min()).apply(lambda x: x.days)
    return df_copy


def plot_auto_corr_all_cols(df):
    def plot_auto_corr(serie, lag=100):
        datax = [serie.autocorr(i) for i in range(lag)]
        plt.plot(datax)

    for name_serie, serie in df.iteritems():
        plot_auto_corr(serie, 350)
        plt.legend(df.columns)


def create_lags_df(serie, lags=5, dropna=False):
    df = pd.DataFrame(index=serie.index)
    for lag in range(lags):
        df[''.join((serie.name, '_', str(lag)))] = serie.shift(lag)
    return df.dropna() if dropna else df


def cross_corr_two_series(s1: pd.Series, s2: pd.Series, lags: int) -> pd.DataFrame:
    """
    :param s1: first time serie
    :param s2: second time serie
    :param lags: number of lags take account
    :return: dataframe of matrix cross-corr
    """
    df1 = create_lags_df(s1, lags=lags, dropna=True)
    df2 = create_lags_df(s2, lags=lags, dropna=True)
    return df1.apply(lambda s: df2.corrwith(s))


