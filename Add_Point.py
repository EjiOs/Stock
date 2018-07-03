import pandas as pd
from pandas import Series, DataFrame
import numpy as np
from datetime import datetime

class Add_Point:
    """ポイント計算のクラス"""

    def point(self,df):
        df['p_n'] = df['平均年収'].apply(self.p_n)
        df['p_a'] = df['平均年齢'].apply(self.p_a)
        df['p_s'] = df['設立年月日'].apply(self.point_s)
        df['p_j'] = df['上場年月日'].apply(self.point_j)
        df['p_t'] = df['時価総額（百万円）'].apply(self.point_total)
        df['p_cf'] = df[['前期営業CF' , '今期営業CF']].apply(self.p_cf , axis = 1)
        df['p_b_sl'] = df[['決算前々期売上高' , '決算前期売上高']].apply(self.p_b_sale , axis = 1)
        df['p_n_sl'] = df[['決算前期売上高' , '決算売上高']].apply(self.p_n_sale , axis = 1)
        df['p_sl'] = df[['決算前々期売上高' , '決算前期売上高' , '決算売上高']].apply(self.p_sale , axis = 1)
        df['p_sp'] = df['少数特定者持株数比率'].apply(self.p_sp)
        df['p_fd'] = df['浮動株数比率'].apply(self.p_fd)
        df['p_self'] = df['自己資本比率'].apply(self.p_self)
        df['p_debt'] = df[['現金同等物' , '有利子負債（百万円）']].apply(self.p_debt , axis = 1)
        df['p_gain_n'] = df[['決算前期営業利益' , '決算営業利益']].apply(self.p_gain_n , axis = 1)
        df['p_gain_NF'] = df[['決算前期営業利益' , '決算営業利益' , '営業利益会社予想']].apply(self.p_gain_NF , axis = 1)
        d = df.columns[26:41]
        df['Points'] = df[d].sum(axis = 1)
        return df

    def p_n (self,n):#平均年収
        if not n == n:
            return 0
        elif n > 601:
            return 0
        elif n > 579:
            return 2
        elif n > 500:
            return 3
        else:
            return 4

    def p_a (self,p):#平均年齢
        if not p == p:
            return 0
        elif p > 46:
            return 0
        elif p > 40:
            return 2
        else:
            return 3

    def point_s (self,s):#設立年月日
        now = datetime.now()
        y50 = datetime(now.year - 50 ,now.month , now.day)
        if not s == s:
            return 0
        elif s > y50:
            return 2
        else:
            return 0

    def point_j (self,j):#上場年月日
        now = datetime.now()
        y10 = datetime(now.year - 10 ,now.month , now.day)
        y20 = datetime(now.year - 20 ,now.month , now.day)
        if not j == j:
            return 0
        elif j > y10:
            return 4
        elif j > y20:
            return 2
        else:
            return 0

    def point_total (self,total):#時価総額
        if not total == total:
            return 0
        elif total > 500000:
            return 0
        elif total > 100000:
            return 1
        elif total > 20000:
            return 3
        elif total > 10000:
            return 4
        elif total > 3000:
            return 5
        elif total <= 3000:
            return 6

    def p_cf (self,cf):#営業CF
        b_cf , n_cf = cf
        if not b_cf == b_cf:
            return 0
        elif not n_cf == n_cf:
            return 0
        elif b_cf > 0 and n_cf > 0:
            return 10
        elif b_cf < 0 and n_cf > 0:
            return 5
        elif b_cf > 0 and n_cf < 0:
            return -5
        elif b_cf < 0 and n_cf < 0:
            return -10

    def p_b_sale (self,sl):#前期増収率
        bb_sl , b_sl = sl
        if not bb_sl == bb_sl:
            return 0
        elif not b_sl == b_sl:
            return 0
        else:
            f_sl = (b_sl - bb_sl)/bb_sl*100
            if f_sl > 20:
                return 9
            elif f_sl > 10:
                return 7
            elif f_sl > 7:
                return 5
            elif f_sl > 3:
                return 1
            elif f_sl < 3:
                return 0

    def p_n_sale (self,sl):#今期増収率
        b_sl , n_sl = sl
        if not b_sl == b_sl:
            return 0
        elif not n_sl == n_sl:
            return 0
        else:
            f_sl = (n_sl - b_sl)/b_sl*100
            if f_sl > 25:
                return 9
            elif f_sl > 15:
                return 7
            elif f_sl > 7:
                return 5
            elif f_sl > 3:
                return 1
            elif f_sl < 3:
                return 0

    def p_sale (self,psl):#増収率変化
        bb_sl , b_sl , n_sl = psl
        if not bb_sl == bb_sl:
            return 0
        elif not b_sl == b_sl:
            return 0
        elif not n_sl == n_sl:
            return 0
        else:
            fb_sl = (b_sl - bb_sl)/bb_sl*100
            fn_sl = (n_sl - b_sl)/b_sl*100
            if fn_sl > fb_sl:
                return 5
            elif fn_sl == fb_sl:
                return 0
            elif fn_sl < fb_sl:
                return -10

    def p_sp (self,sp):#特定株
        if not sp == sp:
            return 0
        elif sp > 60:
            return 3
        elif sp > 50:
            return 2
        else:
            return 0

    def p_fd (self,fd):#浮動株
        if not fd == fd:
            return 0
        elif fd < 17:
            return 3
        elif fd < 25:
            return 2
        else:
            return 0

    def p_self (self,sf):#自己資本比率
        if not sf == sf:
            return 0
        elif sf > 55:
            return 3
        elif sf > 40:
            return 2
        elif sf > 30:
            return 1
        else:
            return 0

    def p_debt (self,db):#借金(有利子負債÷現金同等物で計算)
        gnk , yrs = db
        if not gnk == gnk:
            return 0
        elif not yrs == yrs:
            return 0
        else:
            syk = yrs/gnk
            if syk < 1:
                return 7
            elif syk < 3.5:
                return 3
            else:
                return 0

    def p_gain_n (self,gain):#営業利益増加率(前期÷今期)
        gain_b , gain_n = gain
        if not gain_b == gain_b:
            return 0
        elif not gain_n == gain_n:
            return 0
        else:
            f_gain = (gain_n - gain_b) / abs(gain_b) * 100
            if f_gain > 100:
                return 10
            elif f_gain > 50:
                return 7
            elif f_gain > 15:
                return 5
            elif f_gain > 3:
                return 2
            else:
                return 0

    def p_gain_NF (self,gain):#営業増益率変化(予想増益÷今期増益)
        gain_b , gain_n , gain_f = gain
        if not gain_b == gain_b:
            return 0
        elif not gain_n == gain_n:
            return 0
        elif not gain_f == gain_f:
            return 0
        else:
            f_gain = (gain_n - gain_b) / abs(gain_b) * 100
            ff_gain = (gain_f - gain_n) / abs(gain_n) * 100
            if not f_gain == 0:
                F = (ff_gain - f_gain) / abs(f_gain) * 100
                if F > 20:
                    return 8
                elif F > 10:
                    return 6
                elif F > 0:
                    return 4
                elif F > -15:
                    return 2
                else:
                    return 0
            else:
                return 0
