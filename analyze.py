import csv
import json
import operator
import random

import numpy as np
from sklearn import linear_model
import statistics

MAX = 10000


def print_mean_var(sticker_prices):
    stock_variances = []
    for ticker in sticker_prices:
        open_prices = sticker_prices[ticker]
        if open_prices:
            stock_variances.append((ticker, statistics.mean(open_prices), statistics.variance(open_prices)))
    data = sorted(stock_variances, key=operator.itemgetter(2))
    print '\n'.join([str(a) for a in data])

def load_data_from_file(fn):
    sticker_prices = {}
    with open(fn, 'r') as f:
        cnt = 0
        for l in f:
            cnt += 1
            if cnt > MAX: break
            ticker, data = l.strip().split('\t')
            prices = json.loads(data)
            open_prices = []
            for day in prices:
                if 'Open' in day:
                    # print(ticker, day['Open'])
                    open_prices.append(float(day['Open']))
            sticker_prices[ticker] = open_prices
    return sticker_prices

def find_dips(sticker_prices):
    for ticker in sticker_prices:
        open_prices = sticker_prices[ticker]
        if open_prices:
            pass

def find_rising(sticker_prices, look_back=20, window_size=3):
    rise_count = []
    for ticker in sticker_prices:
        # import pdb; pdb.set_trace()
        open_prices = sticker_prices[ticker][-look_back:]
        if open_prices:
            rise = 0
            drop = 0
            for i in xrange(1 + window_size, len(open_prices)):
                today = sum(open_prices[i - window_size:i])
                yesterday = sum(open_prices[i - 1 - window_size: i - 1])
                if today > yesterday:
                    rise += 1
                else:
                    drop += 1
            gain_percent = float(open_prices[-1] - open_prices[0]) / open_prices[0]
            rise_count.append((ticker, rise, drop, float(rise)/(rise + drop), gain_percent))
    data = sorted(rise_count, key=operator.itemgetter(3), reverse=True)
    print '\n'.join([str(a) for a in data[:10000]])


def find_lr(sticker_prices, look_back=20):
    slopes = []
    for ticker in sticker_prices:
        open_prices = sticker_prices[ticker][:-look_back]
        if open_prices:
            arr_open_prices = np.array(open_prices).reshape(-1, 1)
            arr_X = np.array(range(0, len(open_prices))).reshape(-1, 1)
            lr = linear_model.LinearRegression()
            lr.fit(arr_X, arr_open_prices)
            # print lr.residues_
            slopes.append((ticker, lr.coef_[0][0], lr.residues_[0]))
    data = sorted(slopes, key=operator.itemgetter(1), reverse=True)
    print '\n'.join([str(a) for a in data[:1000]])

if __name__ == '__main__':
    fn = 'updated_prices_tech.csv'
    sticker_prices = load_data_from_file(fn)
    find_rising(sticker_prices)
