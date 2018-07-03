from Add_Point import Add_Point
from Csv_To_Pandas import Csv_To_Pandas
import shelve
import pandas as pd
import datetime as dt

t = dt.date.today()
w = t.weekday()
m = t - dt.timedelta(days = w)
s = shelve.open('Pandas_Data_Frame', writeback = True)
df = s[str(m)+'_df']

df = Csv_To_Pandas().add_csv(df)
df = Csv_To_Pandas().Last_Week_Average(df)
df = Add_Point().point(df)

s[str(m)+'_df'] = df
s.close()
