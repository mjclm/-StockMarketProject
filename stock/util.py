import psutil
import numpy as np
import os
import pandas as pd


def get_memory_usage():
    return np.round(psutil.Process(os.getpid()).memory_info()[0]/2.**30, 2)


def size_of_fmt(num, suffix='B'):
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


def reduce_mem_usage(df, verbose=True):
    def change_nptype_int(np_types):
        for np_type in np_types:
            if np.iinfo(np_type).min < c_min and c_max < np.iinfo(np_type).max:
                df[col] = df[col].astype(np_type)
                break
            else:
                continue

    def change_nptype_float(np_types):
        for np_type in np_types:
            if np.finfo(np_type).min < c_min and c_max < np.finfo(np_type).max:
                df[col] = df[col].astype(np_type)
                break
            else:
                continue

    numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
    start_mem = df.memory_usage().sum() / 1024**2
    for col in df.columns:
        col_type = df[col].dtypes
        if col_type in numerics:
            c_min = df[col].min()
            c_max = df[col].max()
        if 'int' in str(col_type):
            change_nptype_int([np.int8, np.int16, np.int32, np.int64])
        else:
            change_nptype_float([np.float16, np.float32, np.float64])
    end_mem = df.memory_usage().sum() / 1024**2
    if verbose:
        print('Mem. usage decreased to {:5.2f} Mb ({:.1f}% reduction)'
              .format(end_mem, 100 * (start_mem - end_mem) / start_mem))
    return df


def merge_by_concat(df1, df2, merge_on):
    merged_gf = df1[merge_on]
    merged_gf = merged_gf.merge(df2, on=merge_on, how='left')
    new_cols = [col for col in list(merged_gf) if col not in merge_on]
    df1 = pd.concat([df1, merged_gf[new_cols]], axis=1)
    return df1
