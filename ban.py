# -*- coding: utf-8 -*-
import os
import pandas as pd

limitup = 1.1
limitdown = 0.9
tor = 0.0005
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
    records.loc[:,'close'] = records['close'].map(lambda x: round(x, 2))
    records.loc[:,'limit_up'] = records['prev_close'] * limitup
    records.loc[:,'limit_down'] = records['prev_close'] * limitdown
    records.loc[:,'limit_up'] = records['limit_up'].map(lambda x: round(x*(1.0 - tor), 2))
    records.loc[:,'limit_down'] = records['limit_down'].map(lambda x: round(x*(1.0 + tor), 2))
    records.loc[:,'change'] = 100*(records['close'] - records['prev_close']) / records['prev_close']

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
