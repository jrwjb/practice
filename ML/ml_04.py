import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
#导入数据
dataset = pd.read_csv('/Users/wjb/ML/data/Social_Network_Ads.csv')
X = dataset.iloc[:,[2,3]].values
y = dataset.iloc[:,4].values
#拆分数据集
from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size = 0.25,random_state = 0)
#特征缩放
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.fit_transform(X_test)
#使用LR模型
from sklearn.linear_model import LogisticRegression
clf = LogisticRegression()
clf.fit(X_train,y_train)
#预测
y_pred = clf.predict(X_test)
print(clf.score(X_train,y_train),clf.score(X_test,y_test))
#评估模型
#生成混淆矩阵
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test,y_pred)
#可视化
from matplotlib.colors import ListedColormap
X_set,y_set = X_train,y_train
X1,X2 = np.meshgrid(np.arange(start = X_set[:,0].min() - 1,stop = X_set[:,0].max() + 1,step = 0.01),
		    np.arange(start = X_set[:,1].min() - 1,stop = X_set[:,1].max() + 1,step =0.01))
plt.contourf(X1,X2,clf.predict(np.array([X1.ravel(),X2.ravel()]).T).reshape(X1.shape),alpha = 0.75,cmap = ListedColormap(('red','green')))
plt.xlim(X1.min(),X1.max())
plt.ylim(X2.min(),X2.max())
for i,j in enumerate(np.unique(y_set)):
	plt.scatter(X_set[y_set == j,0],X_set[y_set == j,1],c = ListedColormap(('red','green'))(i),label = j)
plt.title('Logistic(training set)')
plt.xlabel('age')
plt.ylabel('estimated salary')
plt.legend()
plt.show()

X_set,y_set = X_test,y_test
X1,X2 = np.meshgrid(np.arange(start = X_set[:,0].min() - 1,stop = X_set[:,0].max() + 1,step = 0.01),
		    np.arange(start = X_set[:,1].min() - 1,stop = X_set[:,1].max() + 1,step = 0.01))
plt.contourf(X1,X2,clf.predict(np.array([X1.ravel(),X2.ravel()]).T).reshape(X1.shape),
		    alpha = 0.75,cmap = ListedColormap(('red','green')))
plt.xlim(X1.min(),X1.max())
plt.ylim(X2.min(),X2.max())
for i,j in enumerate(np.unique(y_set)):
	plt.scatter(X_set[y_set == j,0],X_set[y_set == j,1],c = ListedColormap(('red','green'))(i),label = j)
plt.title('logistic(test set)')
plt.xlabel('age')
plt.ylabel('estimated salary')
plt.legend()
plt.show()
