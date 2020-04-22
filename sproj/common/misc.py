## misc.py
import pandas as pd

def combinations(list1, list2):
    index = []
    for g in list1:
        for d in list2:
            index.append((g, d))

    return index

def replace_nan_none(df):
    df = df.replace({pd.np.nan: None})
    return df