## corelation.py
import common.dates as dates
import common.misc as misc
import pandas as pd
import matplotlib.pyplot as plt
from datetime import timedelta

import database.update as update

from load import prepare_data


class CorMatrix:

    def __init__(self, vix_df, spx_df, tweet_df, group=None, delta=None):
        self.vix_df = vix_df
        self.spx_df = spx_df
        self.tweet_df = tweet_df
        #self.group = group
        #self.delta = delta  # optional
        #self.data = self.prepare_data()

    def delete_dataframes(self):
        self.vix_df, self.spx_df, self.tweet_df = None, None, None

    def prepare_data(self):
        # tweet_df=remove_neutral_sentiment(tweet_df)
        ##self.group_data()
        self.vix_df = self.vix_df.pct_change()  # or pct change?
        self.spx_df = self.spx_df.pct_change()
        return self.concat_data()

    def group_data(self, group):
        # Group data by time period
        self.vix_df = dates.group_data(self.vix_df, ['vix_close'], method='lastValue', group=group)
        self.vix_df.drop(labels='datetime', axis=1, inplace=True)
        self.spx_df = dates.group_data(self.spx_df, ['spx_close'], method='lastValue', group=group)
        self.spx_df.drop(labels='datetime', axis=1, inplace=True)
        self.tweet_df = dates.group_data(self.tweet_df, ['nltk', 'flair'], method='avg', group=group)

    def concat_data(self):
        return pd.concat([self.vix_df, self.spx_df, self.tweet_df], axis=1, sort=True)

    def shift_vix_by_delta(self, delta):
        self.vix_df.datetime = self.vix_df['datetime'] - timedelta(minutes=delta)
        self.vix_df.set_index('datetime', drop=False)

    def shift_spx_by_delta(self, delta):
        self.spx_df.datetime = self.spx_df['datetime'] - timedelta(minutes=delta)
        self.spx_df.set_index('datetime', drop=False)

    def shift_tweet_by_delta(self, delta=None):
        self.tweet_df.datetime = self.tweet_df['datetime'] - timedelta(minutes=delta)
        self.tweet_df.set_index('datetime', drop=False)

    def get_cor_matrix(self, method='pearson'):
        return self.data.corr(method=method)

    def plot_score_vs_spx(self, x='spx', y='vix'):
        self.data.plot(x=x, y=y, kind='scatter')
        plt.show()

def plot_all_cor(data):
    data.unstack(level=0)
    print(data)
    d1 = data["spx:vix"].unstack(level=1)
    xvals = d1.index


def make_data(groups, deltas):
    tuples = misc.combinations(groups, deltas)
    index = pd.MultiIndex.from_tuples(tuples, names=['groups', 'deltas'])
    data = pd.DataFrame(data=0, index=index, columns=['spx:nltk',
                                                      'spx:flair',
                                                      'vix:nltk',
                                                      'vix:flair',
                                                      'spx:vix',
                                                      'nltk:flair'],
                        dtype=float)

    return data


def iterate_cor(cormatrix, data, method):
    """
    DELTA MEASURED IN MINUTES
    :param cormatrix: CorMatrix Object
    :return:
    """
    import copy
    for x in data.index:
        cormatrix_copy = copy.deepcopy(cormatrix)
        group, delta = x[0], x[1]
        cormatrix_copy.shift_spx_by_delta(delta)
        cormatrix_copy.shift_vix_by_delta(delta)
        #cormatrix_copy.shift_tweet_by_delta(delta)
        cormatrix_copy.group_data(group)
        cormatrix_copy.data = cormatrix_copy.prepare_data()
        matrix = cormatrix_copy.get_cor_matrix(method=method)
        data.loc[(group, delta)]['spx:nltk'] = matrix.loc['spx_close']['nltk']
        data.loc[(group, delta)]['spx:flair'] = matrix.loc['spx_close']['flair']
        data.loc[(group, delta)]['vix:nltk'] = matrix.loc['vix_close']['nltk']
        data.loc[(group, delta)]['vix:flair'] = matrix.loc['vix_close']['flair']
        data.loc[(group, delta)]['spx:vix'] = matrix.loc['spx_close']['vix_close']
        data.loc[(group, delta)]['nltk:flair'] = matrix.loc['nltk']['flair']

    return data

def create_corelation_data(groups, deltas):
    """
    neut_sentiment -- "include_neut" or "exclude_neut"
    """
    DATA = {
        'include_neut': {
            'pearson': None,
            'kendall': None,
            'spearman': None},
        'exclude_neut': {
            'pearson': None,
            'kendall': None,
            'spearman': None}
    }

    vix_df, spx_df, tweet_df = prepare_data(remove_neutral_sent=False)
    co = CorMatrix(vix_df, spx_df, tweet_df)
    for method in ['pearson', 'kendall', 'spearman']:
        data = make_data(groups, deltas)
        DATA['include_neut'][method] = iterate_cor(co, data, method)

    vix_df, spx_df, tweet_df = prepare_data(remove_neutral_sent=True)
    co = CorMatrix(vix_df, spx_df, tweet_df)
    for method in ['pearson', 'kendall', 'spearman']:
        data = make_data(groups, deltas)
        DATA['exclude_neut'][method] = iterate_cor(co, data, method)

    return DATA

if __name__ == "__main__":
    vix_df, spx_df, tweet_df = prepare_data()
    co = CorMatrix(vix_df, spx_df, tweet_df)
    groups = ["1T", "5T", "15T", "30T", "60T", "120T", "180T"]#[str(i) + 'T' for i in range(1, 4)]
    deltas = [i for i in range(0, 8)]
    DATA = make_data(groups, deltas)
    DATA = iterate_cor(co, DATA)
    #plot_all_cor(DATA)
    #update.add_corelations(DATA)

    ''' Commented out to debug
if __name__ == "__main__":
    import load
    vix_df1, spx_df1, tweet_df1 = load.prepare_data()
    group = '2T'
    spx_score_cor = {}
    for i in range(1):
        #group = str(i+1)+'T'
        group="213T"
        cor = CorMatrix(vix_df1, spx_df1, tweet_df1, group=group) #doesnt work for 5h weird...
        print(cor.data.loc['2020-04-09'])
        print(cor.data.dropna().std())
        #print(cor.get_cor_matrix(), group)
        spx_score_cor[group] = cor.get_cor_matrix().loc['score']['spx_close']
    #cor.plot_score_vs_spx()
    #print(spx_score_cor)
    #print(max(spx_score_cor.items()))
    '''


    """
    why are there so many nan values for cor?
    Maybe we should standardize dates?
    perhaps we remove nan rows before corelation
    """
