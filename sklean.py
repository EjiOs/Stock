from to_sklean import to_sklean
import sklearn
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error , mean_squared_error ,r2_score
from sklearn.model_selection import train_test_split
import numpy as np
import scipy

sk_df = to_sklean()
lreg = LinearRegression()
X_model = sk_df.drop(['株価変化率','不動産業','名古屋セ'] , 1)
X_model[['平均年齢','自己資本比率','浮動株数比率','少数特定者持株数比率']] = X_model[['平均年齢','自己資本比率','浮動株数比率','少数特定者持株数比率']]*10
X_model = X_model.astype(int)
Y_target = sk_df['株価変化率']*(100)
Y_target = Y_target.astype(int)

X_train , X_test , Y_train , Y_test = train_test_split(X_model , Y_target)
lreg = LinearRegression()
lreg.fit(X_train,Y_train)
pred_train = lreg.predict(X_train)
pred_test = lreg.predict(X_test)

abso = mean_absolute_error(Y_test,pred_test)
squa = mean_squared_error(Y_test , pred_test)
r2 =  r2_score(Y_test,pred_test)

print('平均絶対誤差={:.2f}'.format(abso))
print('平均二乗誤差={:.2f}'.format(squa))
print('決定係数={:.5f}'.format(r2))
