import urllib.request
import datetime as dt
from secret import Secret

url = 'http://kabusapo.com/dl-file/dl-stocklist.php'
#csvに月曜の日付を付ける。
t = dt.date.today()
w = t.weekday()
m = t - dt.timedelta(days = w)
#保存先はデスクトップのPYTHONディレクトリに。
name = Secret().MyDir()[0]
name = name.replace('日付',str(m))
urllib.request.urlretrieve(url,name)
