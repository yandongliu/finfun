import argparse
import csv
from datetime import datetime, timedelta
import json
from operator import itemgetter
import random
import sys
import time

from yahoo_finance import Share


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def get_random_int():
    return random.randint(1, 3)

def read_all_tickers():
    ret = []
    fn = 'Stock.csv'
    with open(fn, 'r') as f:
        for row in csv.DictReader(f):
            ticker = row['Ticker']
            ret.append(ticker)
    return ret

def download_prices_to_today(ticker, prices):
    """Download prices till today.
    :param str ticker:
    :param [dict] prices: prices sorte by date
    """
    try:
        share = Share(ticker)

        # get from_date
        if not prices:
            from_date = datetime.strptime('2015-08-03', '%Y-%m-%d')
        else:
            last_date = datetime.strptime(prices[-1]['Date'], '%Y-%m-%d')
            from_date = (last_date + timedelta(days=1))

        # get to_date
        to_date = datetime.today()
        day_of_week = to_date.weekday()
        if day_of_week == 6:
            to_date = to_date + timedelta(days=-2) # if sunday
        elif day_of_week == 5:
            to_date = to_date + timedelta(days=-1) # if saturday

        # skip if already update-to-date
        if from_date >= to_date:
            return
        str_from_date = from_date.strftime('%Y-%m-%d')
        str_to_date = to_date.strftime('%Y-%m-%d')
        eprint('downloading prices', ticker, str_from_date, str_to_date)
        data = share.get_historical(str_from_date, str_to_date)
        return data
    except Exception as ex:
        eprint(ex)

def get_active_tickers(fn):
    tickers = set([])
    with open(fn, 'r') as f:
        for l in f:
            # import pdb; pdb.set_trace()
            ticker, data = l.strip().split('\t')
            if '.' in ticker:
                continue
            obj = json.loads(data)
            max = 0
            min = 1000
            for o in obj:
                if 'Open' not in o: continue
                open_price = float(o.get('Open'))
                if open_price > max: max = open_price
                if open_price < min: min = open_price
            # print(ticker, len(obj), min, max)
            if min < 1.0: continue
            if max > 1000.0: continue
            if len(obj) < 252:
                continue
            tickers.add(ticker)
    return tickers

def read_active_tickers(fn='active_stocks.txt'):
    stocks = set([])
    with open(fn, 'r') as f:
        for l in f:
            stocks.add(l.strip())
            # if len(stocks) > 1: return stocks
    return stocks

def read_prices_from_file(fn, tickers):
    """read downloaded prices from file. sort by date and return"""
    x = {}
    bad_stocks = set([])
    with open(fn, 'r') as f:
        for l in f:
            ticker, data = l.strip().split('\t')
            if ticker not in tickers: continue
            objs = json.loads(data)
            try:
                x[ticker] = sorted(objs, key=itemgetter('Date'))
                # print(x[ticker][0]['Date'], x[ticker][-1]['Date'])
            except:
                bad_stocks.add(ticker)
    return x, bad_stocks

def update_prices(fn_prices, active_stocks):
    prices, bad_stocks = read_prices_from_file(fn_prices, active_stocks)
    for ticker in read_active_tickers():
        existing_prices = prices.get(ticker) or []
        new_prices = download_prices_to_today(ticker, existing_prices)
        if new_prices:
            existing_prices.extend(new_prices)
            time.sleep(get_random_int())
        print('{}\t{}'.format(ticker, json.dumps(existing_prices)))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--input',
        type=str,
        default='history_prices.csv'
    )
    parser.add_argument(
        '--active_stocks',
        dest='active_stocks',
        action='store_true',
        default=False
    )
    parser.add_argument(
        '--update_prices',
        dest='update_prices',
        action='store_true',
        default=False
    )
    args = parser.parse_args()
    if args.active_stocks:
        tickers = get_active_tickers(fn)
        for t in tickers:
            print(t)
    # download all prices
    if args.update_prices:
        tickers = read_active_tickers()
        eprint('# tickers', len(tickers))
        update_prices(fn_prices=args.input, active_stocks=tickers)
