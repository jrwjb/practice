import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#导入数据
dataset = pd.read_csv('/Users/wjb/ML/data/Social_Network_Ads.csv')
X = dataset.iloc[:,[2,3]].values
y = dataset.iloc[:,4].values
#拆分数据
from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size = 0.25,random_state = 0)
#特征量化
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.fit_transform(X_test)
#svm 模型
from sklearn.svm import SVC
clf = SVC(kernel = 'linear',random_state = 0)
clf.fit(X_train,y_train)
#预测结果
y_pred = clf.predict(X_test)
#创建混淆矩阵
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test,y_pred)
#可视化
from matplotlib.colors import ListedColormap
X_set,y_set = X_train,y_train
X1,X2 = np.meshgrid(np.arange(start = X_set[:,0].min()-1,stop = X_set[:,0].max()+1,step=0.01),np.arange(start = X_set[:,1].min()-1,stop = X_set[:,1].max()+1,step=0.01))
plt.contourf(X1,X2,clf.predict(np.array([X1.ravel(),X2.ravel()]).T).reshape(X1.shape),alpha = 0.75,cmap = ListedColormap(('red','green')))
plt.xlim(X1.min(),X1.max())
plt.ylim(X2.min(),X2.max())
for i,j in enumerate(np.unique(y_set)):
	plt.scatter(X_set[y_set == j,0],X_set[y_set == j,1],c = ListedColormap(('red','green'))(i),label = j)
plt.title('svm(train set)')
plt.xlabel('age')
plt.ylabel('estimated salary')
plt.legend()
plt.show()

