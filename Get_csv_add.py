import urllib.request
import datetime as dt
url = ''
#csvに月曜の日付を付ける。
t = dt.date.today()
w = t.weekday()
m = t - dt.timedelta(days = w)
#保存先はデスクトップのPYTHONディレクトリに。
name = '/Users/eiji/Desktop/PYTHON/日付.csv'
name = name.replace('日付',str(m))
urllib.request.urlretrieve(url,name)
