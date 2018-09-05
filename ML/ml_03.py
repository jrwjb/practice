import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#导入数据
dataset = pd.read_csv('/Users/wjb/ML/data/data_03.csv')
X = dataset.iloc[:,:-1].values
y = dataset.iloc[:,4].values
#将类别数据数字化
from sklearn.preprocessing import LabelEncoder,OneHotEncoder
labelencoder = LabelEncoder()
X[:,3] = labelencoder.fit_transform(X[:,3])
onehotencoder = OneHotEncoder(categorical_features = [3])
X = onehotencoder.fit_transform(X).toarray()
#躲避虚拟变量陷阱
X = X[:,1:]
#拆分数据集
from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size = 0.2,random_state = 0)
#训练多元回归模型
from sklearn.linear_model import LinearRegression
regressor = LinearRegression()
regressor.fit(X_train,y_train)
#在测试集上预测结果
y_pred = regressor.predict(X_test)
print(regressor.score(X_train,y_train),'\n',regressor.score(X_test,y_test))
