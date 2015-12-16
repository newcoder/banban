# -*- coding: utf-8 -*-
import os
import pandas as pd

path = 'SH600055.csv'
limitup = 1.1
limitdown = 0.9
columns = ['date', 'open', 'low', 'high', 'close', 'volume', 'amount']

def get_bans(path):
    records = pd.read_table(path, sep=',', header=0, names=columns)
    records['prev_close'] = records.close.shift(1)
    records['limit_up'] = records['prev_close'] * limitup
    records['limit_down'] = records['prev_close'] * limitdown
    records['change'] = 100*(records['close'] - records['prev_close']) / records['prev_close']

    up_bans = records[records['close'] >= records['limit_up']]
    down_bans = records[records['close'] <= records['limit_down']]

    # kbody == 0 and kshadow == 0 means 一字板
    up_bans.loc[:,'kbody'] = 100*(up_bans['close'] - up_bans['open']) / up_bans['prev_close']
    down_bans.loc[:,'kbody'] = 100*(down_bans['close'] - down_bans['open']) / down_bans['prev_close']
    up_bans.loc[:,'kshadow'] = 100*(up_bans['open'] - up_bans['low']) / up_bans['prev_close']
    down_bans.loc[:,'kshadow'] = 100*(down_bans['open'] - down_bans['high']) / down_bans['prev_close']

    return pd.concat([up_bans, down_bans])

def get_bans_dir(dir):
    filelist = os.listdir(dir)
    dflist = []
    results = pd.DataFrame()
    for file in filelist:
        if file.startswith('SZ300') or file.startswith('SZ000') or file.startswith('SZ002') \
        or file.startswith('SH600') or file.startswith('SH601') or file.startswith('SH603'):
            bans = get_bans(dir + '\\' + file)
            bans.insert(0, 'symbol', file[:-4])
            dflist.append(bans)
            print file + ' done!'
    results = pd.concat(dflist).sort_values(by=['symbol', 'date'])
    return results
