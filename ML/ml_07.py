import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#导入数据
dataset = pd.read_csv('/Users/wjb/ML/data/Social_Network_Ads.csv')
X = dataset.iloc[:,[2,3]].values
y = dataset.iloc[:,4].values
#拆分数据集
from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.25,random_state = 0)
#特征缩放
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)
#使用KNN对模型
from sklearn.neighbors import KNeighborsClassifier
clf = KNeighborsClassifier(n_neighbors = 5,metric = 'minkowski',p = 2)
clf.fit(X_train,y_train)

#预测测试集
y_pred = clf.predict(X_test)
#生成混淆矩阵
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test,y_pred)

print(clf.score(X_test,y_pred))

