import shelve
import pandas as pd
import numpy as np
import datetime as dt
from datetime import date , timedelta
import scipy

def to_sklean():
    s = shelve.open('Pandas_Data_Frame')
    df = s['2018-07-23_df']
    s.close()

    df = df.drop(df.columns[1:2] , 1)
    df = df.drop(df.columns[40:] , 1)

    df_csv = pd.read_csv('/Volumes/webdav/kabu.plus/csv/japan-all-stock-prices/daily/japan-all-stock-prices.csv', encoding = 'shift-jis')
    df_csv.drop([0,1] , 0 , inplace = True)
    df_csv.drop(df_csv.columns[1:5] , 1 , inplace = True)
    df_csv.drop(df_csv.columns[2:] , 1 , inplace = True)

    df = pd.merge(df,df_csv,on='SC',how='left')
    df.replace('-' , np.nan , inplace = True)
    df['株価'] = df['株価'].astype(float)

    def up_down (ud):
        bef , now = ud
        updown = (now - bef)/bef*100
        updown = round(updown , 2)#少数第2位までにした
        return updown

    df['株価変化率'] = df[['週平均','株価']].apply(up_down , axis = 1)
    trade_dummies = pd.get_dummies(df['業種分類'])
    market_dummies = pd.get_dummies(df['市場名'])
    dummies = pd.concat([trade_dummies,market_dummies],axis = 1)
    df = pd.concat([df,dummies] , axis = 1)
    df = df.drop(['SC','市場名','業種分類','設立年月日','上場年月日','週平均','株価'],1)

    df.dropna(subset = ['平均年齢','平均年収','時価総額（百万円）','株価変化率'] , inplace = True)
    df.fillna(0 , inplace=True)

    return df
