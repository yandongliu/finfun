import csv
import json
import operator
import random
import statistics

MAX = 100000


def print_mean_var(fn):
    stock_variances = []
    with open(fn, 'r') as f:
        cnt = 0
        for l in f:
            cnt += 1
            if cnt > MAX: break
            ticker, data = l.strip().split('\t')
            days = json.loads(data)
            open_prices = []
            for day in days:
                if 'Open' in day:
                    # print(ticker, day['Open'])
                    open_prices.append(float(day['Open']))
            stock_variances.append((ticker, statistics.mean(open_prices), statistics.variance(open_prices)))
    data = sorted(stock_variances, key=operator.itemgetter(2))
    print('\n'.join([str(a) for a in data]))

def find_dips(fn):
    # TODO
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
            stock_variances.append((ticker, statistics.mean(open_prices), statistics.variance(open_prices)))
    data = sorted(stock_variances, key=operator.itemgetter(2))
    print('\n'.join([str(a) for a in data]))

fn = 'updated_prices.csv'
print_mean_var(fn)
