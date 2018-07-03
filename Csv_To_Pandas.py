import pandas as pd
from pandas import Series, DataFrame
#import datetime as dt
from datetime import date , timedelta
import numpy as np
import shelve
import re
from secret import Secret

class Csv_To_Pandas:
    name = Secret().MyDir()[0]
    t = date.today()
    w = t.weekday()
    monday = t - timedelta(days = w)
    #CSVをデータフレームにする。そのときに不要な項目も削除。
    def csv_remake(self):
        csv_name = self.name.replace('日付',str(self.monday))
        csv_data = pd.read_csv(csv_name)
        new_df = csv_data.drop(['単元株数','日経225採用銘柄'],axis = 1)
        new_df = new_df.rename(columns = {'銘柄コード' : 'SC'})
        return new_df
    #過去のデータと比較して銘柄の増減をチェック。
    def to_pandas(self,new_df):
        s = shelve.open('Pandas_Data_Frame')
        last_mon = self.monday - timedelta(days = 7)
        last_mon_df = str(last_mon) + '_df'
        base_df = s[last_mon_df]
        #set関数？を使うことで増減をチェック。
        base_set = set(base_df['SC'])
        new_set = set(new_df['SC'])

        e = sorted(list(base_set|new_set))#足して重複をなくした完成形の全体像。
        d = base_set^new_set#増えたり減ったりした銘柄。
        #print(len(e))
        man_l = d-base_set#newが増えてたパターン
        few_l = d-new_set#newが減ってたパターン

        if len(man_l) != 0:#newが増えてたパターン
            self.many_line(s,man_l,e,new_df,base_df,last_mon)
            return new_df
        if len(few_l) != 0:#newが減ってたパターン
            return self.few_line(few_l,e,new_df,base_df)
        if len(man_l)+len(few_l) == 0:#増減が無かったパターン
            return new_df
        s.close()

    ##newが増えてたパターン
    def many_line(self,shel,man_list,e,m_new_df,m_base_df,last_monday):
        startday = date(2018,4,2)#データ収集基準日。
        a = self.monday - startday
        a = a.days
        for aa in list(man_list):
            f = e.index(aa)
            line = m_new_df.loc[f:f]
            for mon in range(0,a,7):#基準日から今までの作成されたデータフレームの修正をする。
                m = startday + timedelta(days = mon)
                df_name = str(m) + '_df'
                shel[df_name] =  pd.concat([shel[df_name].iloc[:f],line,shel[df_name].iloc[f:]]).reset_index(drop=True)
                shel[df_name] = shel[df_name].loc[:,['SC','銘柄名','市場名','業種分類','前期営業CF','今期営業CF','前期投資CF','今期投資CF','決算前々期売上高','決算前期売上高','決算売上高','売上高会社予想','現金同等物','決算前期営業利益','決算営業利益','営業利益会社予想','設立年月日','上場年月日','平均年齢','平均年収']]

    #newが減ってたパターン
    def few_line(self,few_list,e,f_new_df,f_base_df):
        for bb in list(few_list):
            g = e.index(bb)
            line = f_base_df.loc[g:g]
            f_new_df = pd.concat([f_new_df.iloc[:g],line,f_new_df.iloc[g:]]).reset_index(drop=True)
        new_df = f_new_df.drop(['前期営業CF','今期営業CF','前期投資CF','今期投資CF','決算前々期売上高','決算前期売上高','決算売上高','売上高会社予想','現金同等物','決算前期営業利益','決算営業利益','営業利益会社予想','設立年月日','上場年月日','平均年齢','平均年収'],axis = 1)
        new_df = new_df.loc[:,['SC','銘柄名','市場名','業種分類']]

        return new_df


    def add_csv(self,df):
        '''
        KABU+のページとリンクしている共有フォルダからCSVデータを取得、必要な情報のみに修正している。
        '''
        dir , prices , results , ratio , daily = Secret().MyDir()
        df_all = pd.read_csv(prices , encoding = 'shift-jis')#別のcsvから時価総額だけ抽出する。
        df_all.drop([0,1] , inplace = True)
        df_all.drop(df_all.columns[1:14] , axis = 1 , inplace = True)
        df_all.drop(df_all.columns[2:4] , axis = 1 , inplace = True)
        df_all = df_all.replace({'-' : np.nan , 0 : np.nan})
        df_all['時価総額（百万円）'] = df_all['時価総額（百万円）'].astype(float)

        df_all_s = pd.read_csv(results , encoding = 'shift-jis')#別のcsvから抽出する。
        df_all_s.drop(df_all_s.columns[1:11] , axis = 1 , inplace = True)
        df_all_s.drop(df_all_s.columns[3:6] , axis = 1 , inplace = True)
        df_all_s = df_all_s.replace({'-' : np.nan , 0 : np.nan})
        for n in list(df_all_s.columns[1:3]):
            df_all_s[n] = df_all_s[n].astype(float)

        df_ratio = pd.read_csv(ratio , encoding = 'shift-jis')#別のcsvから抽出する。これはエンコードを指定する。
        df_ratio.drop(df_ratio.columns[3:5] , axis = 1 , inplace = True)
        df_ratio = df_ratio.replace({'-' : np.nan})
        for m in list(df_ratio.columns[1:3]):
            df_ratio[m] = df_ratio[m].str.replace('%' , '')
            df_ratio[m] = df_ratio[m].astype(float)

        df = df.replace(r'歳|万円|\n\t+|\n+|,' , '' , regex = True)#正規表現
        df = df.replace({'-' : np.nan , '--' : np.nan , '0' : np.nan })#辞書型

        a = list(df.columns[4:16]) + list(df.columns[18:20])
        for n in a:
            df[n] = df[n].astype(float)

        for m in list(df.columns[16:18]):
            for c in df[m]:
                if not '月' in str(c):
                    df.replace(c , np.nan , inplace = True)
                elif not str(c).endswith('日'):#'日' in str(c):
                    df.replace(c , str(c)+'1日' , inplace = True)

        for n in list(df.columns[16:18]):
            df[n] = pd.to_datetime(df[n] , format = '%Y年%m月%d日')

        df = pd.merge(df , df_all , on = 'SC' ,how = 'outer')
        df = pd.merge(df , df_all_s , on = 'SC' ,how = 'outer')
        df = pd.merge(df , df_ratio , on = 'SC' ,how = 'outer')
        df = df.sort_values(by = 'SC')
        df.reset_index(inplace = True , drop = True)
        return df

    def Last_Week_Average(self , df):
        '''
        前週の株価を週平均にして返す。元データはKABU+の共有フォルダから取得。
        tryやlenの部分は祝日のある週の対応をしている。
        '''
        daily = Secret().MyDir()[4]
        now = date.today()
        m1 = now - timedelta(weeks = 1)
        w1 = m1.weekday()
        m1mon = m1 - timedelta(days = w1)

        csv = 'japan-all-stock-prices_日付.csv'
        m1dfList = []
        for n in range(5):
            m1week = m1mon + timedelta(days = n)
            m1weekstr = str(m1week).replace('-' , '')
            csv_m1 = csv.replace('日付' , m1weekstr)
            try:
                Ls_df = pd.read_csv(daily + csv_m1 , encoding = 'shift-jis')
            except FileNotFoundError:
                pass
            else:
                m1dfList.append(Ls_df)

        L = len(m1dfList)

        for n in range(L):
            m1dfList[n].drop([0,1] , 0 ,inplace = True)
            m1dfList[n].drop(m1dfList[n].columns[1:5] , 1 , inplace = True)
            m1dfList[n].drop(m1dfList[n].columns[2:] , 1 , inplace = True)

        Ave_df = pd.merge(m1dfList[0] , m1dfList[1] , on = 'SC' ,how = 'outer')
        for n in range(2 , L):
            Ave_df = pd.merge(Ave_df , m1dfList[n] , on = 'SC' ,how = 'outer')
        Ave_df.replace('-' , np.nan ,inplace = True)

        colLis = ['SC']
        for n in range(L):
            colLis.append('株価' + str(n + 1))
        Ave_df.columns = colLis

        N = len(m1dfList)+1
        d = Ave_df.columns[1:N]
        for c in d:
            Ave_df[c] = Ave_df[c].astype(float)
        Ave_df['週平均'] = Ave_df[d].mean(axis = 1)
        Ave_df.drop(Ave_df.columns[1:N] , axis = 1 , inplace = True)
        df = pd.merge(df , Ave_df , on = 'SC' ,how = 'outer')
        df = df.sort_values(by = 'SC')
        df.reset_index(inplace = True , drop = True)
        return df
