from Csv_To_Pandas import Csv_To_Pandas
import datetime
from Web_Data_Get import Web_Data_Get
import shelve
import datetime as dt
#自作クラスをインスタンス化、csvをデータフレームに直す。
new_df = Csv_To_Pandas().csv_remake()
new_df = Csv_To_Pandas().to_pandas(new_df)
#まずはWebからデータ収集、リストに収納。
L = list(new_df['SC'])
all_get_list = [Web_Data_Get(c).all_get2() for c in L]
sum_get_list = [Web_Data_Get(c).summary_get() for c in L]
#楽天はIDが必要なので、違う方法で収集。
URL = Web_Data_Get('1301').raku_url_get().replace('1301','01')
rk_get_list = [Web_Data_Get(c).raku_data(URL) for c in L]
#リストに収納したデータを振り分け。
new_df['前期営業CF'] = [all_get_list[a][0] for a in range(len(L))]
new_df['今期営業CF'] = [all_get_list[a][1] for a in range(len(L))]
new_df['前期投資CF'] = [all_get_list[a][2] for a in range(len(L))]
new_df['今期投資CF'] = [all_get_list[a][3] for a in range(len(L))]
new_df['決算前々期売上高'] = [all_get_list[a][4] for a in range(len(L))]
new_df['決算前期売上高'] = [all_get_list[a][5] for a in range(len(L))]
new_df['決算売上高'] = [all_get_list[a][6] for a in range(len(L))]
new_df['売上高会社予想'] = [rk_get_list[a][3] for a in range(len(L))]
#[Web_Data_Get(c).raku_data(URL)[3] for c in L]
new_df['現金同等物'] = [all_get_list[a][7] for a in range(len(L))]
new_df['決算前期営業利益'] = [rk_get_list[a][0] for a in range(len(L))]
new_df['決算営業利益'] = [rk_get_list[a][1] for a in range(len(L))]
new_df['営業利益会社予想'] = [rk_get_list[a][2] for a in range(len(L))]
#ここからまたデータの振り分け。
new_df['設立年月日'] = [sum_get_list[a][0] for a in range(len(L))]
new_df['上場年月日'] = [sum_get_list[a][1] for a in range(len(L))]
new_df['平均年齢'] = [sum_get_list[a][2] for a in range(len(L))]
new_df['平均年収'] = [sum_get_list[a][3] for a in range(len(L))]

#new_df = Csv_To_Pandas().add_csv(new_df)
#new_df = Add_Point().point(new_df)

#月曜の日付を使って名前保存。
t = dt.date.today()
w = t.weekday()
m = t - dt.timedelta(days = w)
s = shelve.open('Pandas_Data_Frame')
s[str(m)+'_df'] = new_df
s.close()
#テスト用に追記
