import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#数据预处理
dataset = pd.read_csv('/Users/wjb/ML/data/studentscores.csv')
X = dataset.iloc[:,:1].values
y = dataset.iloc[:,1].values

from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size = 1/4,random_state = 0)
#使用线性回归
from sklearn.linear_model import LinearRegression
regressor = LinearRegression()
regressor = regressor.fit(X_train,y_train)
#预测结果
y_pred = regressor.predict(X_test)
#训练结果可视化
plt.scatter(X_train,y_train,color = 'red')
plt.plot(X_train,regressor.predict(X_train),color = 'blue')
plt.title('Train')
plt.show()
#测试结果可视化
print(X_test.shape,y_test.shape)
plt.scatter(X_test,y_test,color = 'red')
plt.plot(X_test,regressor.predict(X_test),color = 'blue')
plt.title('Test')
plt.show()
