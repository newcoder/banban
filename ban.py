# -*- coding: utf-8 -*-
import os
import pandas as pd

limitup = 1.1
limitdown = 0.9
tor = 0.005
columns = ['date', 'open', 'low', 'high', 'close', 'volume', 'amount']

def is_valid(df):
    return len(df[df.low < 0]) == 0

def get_bans(path):
    records = pd.read_table(path, sep=',', header=0, names=columns)
    # skip this stock when there is invalid data
    if not is_valid(records):
        return -1, None;

    records.loc[:,'prev_close'] = records.close.shift(1)
    records.loc[:,'prev_close'] = records['prev_close'].map(lambda x: round(x, 2))
    records.loc[:,'next_close'] = records.close.shift(-1)
    records.loc[:,'next_close'] = records['next_close'].map(lambda x: round(x, 2))
    records.loc[:,'close'] = records['close'].map(lambda x: round(x, 2))
    records.loc[:,'limit_up'] = records['prev_close'] * limitup
    records.loc[:,'limit_down'] = records['prev_close'] * limitdown
    records.loc[:,'limit_up'] = records['limit_up'].map(lambda x: round(x*(1.0 - tor), 2))
    records.loc[:,'limit_down'] = records['limit_down'].map(lambda x: round(x*(1.0 + tor), 2))
    records.loc[:,'percent'] = 100*(records['close'] - records['prev_close']) / records['prev_close']
    records.loc[:,'next_percent'] = 100*(records['next_close'] - records['close']) / records['close']

    up_bans = records[records['close'] >= records['limit_up']]
    down_bans = records[records['close'] <= records['limit_down']]

    # kbody == 0 and kshadow == 0 means 一字板
    up_bans.loc[:,'kbody'] = 100*(up_bans['close'] - up_bans['open']) / up_bans['prev_close']
    down_bans.loc[:,'kbody'] = 100*(down_bans['close'] - down_bans['open']) / down_bans['prev_close']
    up_bans.loc[:,'kshadow'] = 100*(up_bans['open'] - up_bans['low']) / up_bans['prev_close']
    down_bans.loc[:,'kshadow'] = 100*(down_bans['open'] - down_bans['high']) / down_bans['prev_close']

    bans = pd.concat([up_bans, down_bans])
    return len(records), bans

def get_bans_dir(dir):
    filelist = os.listdir(dir)
    dflist = []
    nums = []
    results = pd.DataFrame()
    for file in filelist:
        if file.startswith('SZ300') or file.startswith('SZ000') or file.startswith('SZ002') \
        or file.startswith('SH600') or file.startswith('SH601') or file.startswith('SH603'):
            rec_nums, bans = get_bans(dir + '\\' + file)
            if rec_nums < 0:
                print file + ' data invalid!!!'
                continue
            bans.insert(0, 'symbol', file[:-4])
            dflist.append(bans)
            nums.append(rec_nums)
            print file + ' done!'
    results = pd.concat(dflist).sort_values(by=['symbol', 'date'])
    return nums, results

def get_all_bans():
    sh_nums, sh_bans = get_bans_dir("data\\SH")
    sz_nums, sz_bans = get_bans_dir("data\\SZ")
    return sum(sh_nums) + sum(sz_nums), pd.concat([sh_bans, sz_bans]).reset_index(drop=True)

def count_by_date(bans):
    datesymbol= bans[list(['symbol','date', 'percent'])]
    countbydate = datesymbol.groupby('date').count()
    countbydate.sort_values(by='symbol', inplace=True, ascending=False)
    return countbydate

def gf_last_digit(df, ind, col):
    value = df[col].loc[ind]
    return value[-1]

def gf_up_down(df, ind, col):
    if (df[col].loc[ind] > 0):
        return 'UP'
    else:
        return 'DOWN'

def group_by_last_digit(bans):
    return bans.groupby(lambda x: gf_last_digit(bans, x, 'symbol'))

def group_by_up_down(bans):
    return bans.groupby(lambda x: gf_up_down(bans, x, 'percent'))

def group_by_last_digit_up_down(bans):
    return bans.groupby([lambda x: gf_last_digit(bans, x, 'symbol'), lambda x: gf_up_down(bans, x, 'percent')])

def count_by_date_up_down(bans):
    datesymbol= bans[list(['symbol','date', 'percent'])]
    countbydate = datesymbol.groupby(['date', lambda x: gf_up_down(bans, x, 'percent')]).count()
    countbydate.sort_values(by=['symbol'], inplace=True, ascending=False)
    return countbydate

def export(bans, file):
    bans.sort_values(by='date').reset_index(drop=True).to_csv(file)
