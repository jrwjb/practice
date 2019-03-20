import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np
import pandas as pd
import warnings

## 使用sklearn中的PolynomialFeatures
def poly(file):
    dataset = pd.read_csv(file)
    X = np.asarray(dataset.get('x'))
    y = np.asarray(dataset.get('y'))

    # 划分训练集和测试集
    X_train = X[:-30]
    X_test = X[-30:]
    y_train = y[:-30]
    y_test = y[-30:]

    # # fit_intercept 为 True
    # model1 = Pipeline([('poly', PolynomialFeatures(degree=2)), ('linear', LinearRegression(fit_intercept=True))])
    # model1 = model1.fit(X_train[:, np.newaxis], y_train)
    # y_test_pred1 = model1.named_steps['linear'].intercept_ + model1.named_steps['linear'].coef_[1] * X_test
    # print('Coefficients: ', model1.named_steps['linear'].coef_)
    # print('Intercept:', model1.named_steps['linear'].intercept_)
    # print('the model is: y = ', model1.named_steps['linear'].intercept_, ' + ', model1.named_steps['linear'].coef_[1],
    #       '* X')
    # # , '+', model1.named_steps['linear'].coef_[2], '* X2', '+', model1.named_steps['linear'].coef_[3], '* X3'
    #
    # # 均方误差
    # print("Mean squared error: %.2f" % mean_squared_error(y_test, y_test_pred1))
    # # r2 score，0,1之间，越接近1说明模型越好，越接近0说明模型越差
    # print('Variance score: %.2f' % r2_score(y_test, y_test_pred1), '\n')

    # fit_intercept 为 False
    model2 = Pipeline([('poly', PolynomialFeatures(degree=3)), ('linear', LinearRegression(fit_intercept=False))])
    model2 = model2.fit(X_train[:, np.newaxis], y_train)
    y_test_pred2 = model2.named_steps['linear'].coef_[0] + model2.named_steps['linear'].coef_[1] * X_test + \
                   model2.named_steps['linear'].coef_[2] * X_test * X_test + model2.named_steps['linear'].coef_[3] * X_test * X_test * X_test
    print('Coefficients: ', model2.named_steps['linear'].coef_)
    print('Intercept:', model2.named_steps['linear'].intercept_)
    print('the model is: y = ', model2.named_steps['linear'].coef_[0], '+', model2.named_steps['linear'].coef_[1],
          '* X + ',
          model2.named_steps['linear'].coef_[2], '* X^2', '+', model2.named_steps['linear'].coef_[3], '* X^3')
    # 均方误差
    print("Mean squared error: %.2f" % mean_squared_error(y_test, y_test_pred2))
    # r2 score，0,1之间，越接近1说明模型越好，越接近0说明模型越差
    print('Variance score: %.2f' % r2_score(y_test, y_test_pred2), '\n')

    # print(round(model2.named_steps['linear'].coef_[0], 2))

    plt.xlabel('x')
    plt.ylabel('y')
    # 画训练集的散点图
    plt.scatter(X_train, y_train, alpha=0.8, color='black')
    # 画模型
    plt.plot(X_train, model2.named_steps['linear'].coef_[0] + model2.named_steps['linear'].coef_[1] * X_train +
             model2.named_steps['linear'].coef_[2] * X_train * X_train + model2.named_steps['linear'].coef_[3] * X_train * X_train * X_train, color='green',
             linewidth=1)
    plt.show()

file = 'C:\\Users\\jbwang\\Desktop\\lousai-22-01.csv'
poly(file)

### 数学解法
dataset = pd.read_csv('C:\\Users\\jbwang\\Desktop\\lousai-22-01.csv')
X = np.asarray(dataset.get('x')).reshape(-1, 1)
y = np.asarray(dataset.get('y'))
# print(X)
# 扩展X
Z = np.column_stack((X, X ** 2, X ** 3))
# 为X增加一列全为1，来求偏置项
Z = np.column_stack((Z, np.ones(len(X))))
# print(Z)
# 划分训练集和测试集
Z_train = Z[:-30]
Z_test = Z[-30:]
y_train = y[:-30]
y_test = y[-30:]

Z_train = np.mat(Z_train)
y_train = np.mat(y_train).T

xTx = Z_train.T * Z_train
w = 0
if np.linalg.det(xTx) == 0.0:
    print('xTx不可逆')
else:
    w = np.ravel(xTx.I * (Z_train.T * y_train))
coef_ = w[:-1]
intercept_ = w[-1]

# 去掉添加的那一列1

Z_train = Z_train[:, 0:3]
Z_test = Z_test[:, 0:3]
# print(Z_train)
# print(coef_)
y_test_pred = coef_[0] * Z_test[:, 0] + coef_[1] * Z_test[:, 1] + coef_[2] * Z_test[:, 2] + intercept_
# print(y_test, y_test_pred)
# 矩阵转回数组
Z_train = np.ravel(Z_train)
y_train = np.ravel(y_train)

print('Coefficients: ', coef_)
print('Intercept:', intercept_)
print('the model is: y = ', coef_[0], '* X + ', coef_[1], '* X^2 + ', coef_[2], '* X^3 + ', intercept_)
# 均方误差
print("Mean squared error: %.2f" % np.average((y_test - y_test_pred) ** 2))

plt.xlabel('x')
plt.ylabel('y')
# 画训练集的散点图

X_train = X[:-30]
plt.scatter(X_train, y_train, alpha=0.8, color='black')
# 画模型
plt.plot(X_train, intercept_ + coef_[0] * X_train + coef_[1] * X_train * X_train + coef_[2] * X_train * X_train * X_train, color='green', linewidth=1)

plt.show()

##### 其他方法
# from numpy import *
# def Data(file):
#     dataset = pd.read_csv(file)
#     X = np.asarray(dataset.get('x'))
#     y = np.asarray(dataset.get('y'))
#
#     # 划分训练集和测试集
#     X_train = X[:-30]
#     X_test = X[-30:]
#     y_train = y[:-30]
#     y_test = y[-30:]
#     return X_train, y_train, X_test, y_test
#
# def MAT(x,y,order):
#     X=[]
#     for i in range(order+1):
#         X.append(x**i)
#     X=mat(X).T
#     Y=array(y).reshape((len(y),1))
#     return X,Y
# def fig(x1,y1,x2,y2):
#     plt.xlabel('X')
#     plt.ylabel('Y')
#     plt.plot(x1,y1,color='g',linestyle='-',marker='')
#     plt.plot(x2,y2,color='m',linestyle='',marker='.')
#     plt.grid()
#     plt.show()
# def Solve():
#     x,y,xr,yr = Data(file)
#     X,Y = MAT(x,y,3)
#     XT=X.transpose()
#     B=dot(dot(linalg.inv(dot(XT,X)),XT),Y)
#     myY=dot(X,B)
#     fig(x,myY,xr,yr)
#
# # Solve()
#
# '''
# 高斯列主消元算法
# '''
# # 得到增广矩阵
# def get_augmented_matrix(matrix, b):
#     row, col = np.shape(matrix)
#     matrix = np.insert(matrix, col, values=b, axis=1)
#     return matrix
# # 取出增广矩阵的系数矩阵（第一列到倒数第二列）
# def get_matrix(a_matrix):
#     return a_matrix[:, :a_matrix.shape[1] - 1]
# # 选列主元，在第k行后的矩阵里，找出最大值和其对应的行号和列号
# def get_pos_j_max(matrix, k):
#     max_v = np.max(matrix[k:, :])
#     pos = np.argwhere(matrix == max_v)
#     i, _ = pos[0]
#     return i, max_v
# # 矩阵的第k行后，行交换
# def exchange_row(matrix, r1, r2, k):
#     matrix[[r1, r2], k:] = matrix[[r2, r1], k:]
#     return matrix
# # 消元计算(初等变化)
# def elimination(matrix, k):
#     row, col = np.shape(matrix)
#     for i in range(k + 1, row):
#         m_ik = matrix[i][k] / matrix[k][k]
#         matrix[i] = -m_ik * matrix[k] + matrix[i]
#     return matrix
# # 回代求解
# def backToSolve(a_matrix):
#     matrix = a_matrix[:, :a_matrix.shape[1] - 1]  # 得到系数矩阵
#     b_matrix = a_matrix[:, -1]  # 得到值矩阵
#     row, col = np.shape(matrix)
#     x = [None] * col  # 待求解空间X
#     # 先计算上三角矩阵对应的最后一个分量
#     x[-1] = b_matrix[col - 1] / matrix[col - 1][col - 1]
#     # 从倒数第二行开始回代x分量
#     for _ in range(col - 1, 0, -1):
#         i = _ - 1
#         sij = 0
#         xidx = len(x) - 1
#         for j in range(col - 1, i, -1):
#             sij += matrix[i][j] * x[xidx]
#             xidx -= 1
#         x[xidx] = (b_matrix[i] - sij) / matrix[i][i]
#     return x
# # 求解非齐次线性方程组：ax=b
# def solve_NLQ(a, b):
#     a_matrix = get_augmented_matrix(a, b)
#     for k in range(len(a_matrix) - 1):
#         # 选列主元
#         max_i, max_v = get_pos_j_max(get_matrix(a_matrix), k=k)
#         # 如果A[ik][k]=0，则矩阵奇异退出
#         if a_matrix[max_i][k] == 0:
#             print('矩阵A奇异')
#             return None, []
#         if max_i != k:
#             a_matrix = exchange_row(a_matrix, k, max_i, k=k)
#         # 消元计算
#         a_matrix = elimination(a_matrix, k=k)
#     # 回代求解
#     X = backToSolve(a_matrix)
#     return a_matrix, X
#
# def init_fx_data(file):
#     dataset = pd.read_csv(file)
#     X = np.asarray(dataset.get('x'))
#     y = np.asarray(dataset.get('y'))
#     return X, y
#
# # 计算最小二乘法当前的误差
# def last_square_current_loss(xs, ys, A):
#     error = 0.0
#     for i in range(len(xs)):
#         y1 = 0.0
#         for k in range(len(A)):
#             y1 += A[k] * xs[i] ** k
#         error += (ys[i] - y1) ** 2
#     return error
#
# # 数学解法：最小二乘法+求解线性方程组
# def last_square_fit_curve_Gauss(xs, ys, order):
#     X, Y = [], []
#     # 求解偏导数矩阵里，含有xi的系数矩阵X
#     for i in range(0, order + 1):
#         X_line = []
#         for j in range(0, order + 1):
#             sum_xi = 0.0
#             for xi in xs:
#                 sum_xi += xi ** (j + i)
#             X_line.append(sum_xi)
#         X.append(X_line)
#     # 求解偏导数矩阵里，含有yi的系数矩阵Y
#     for i in range(0, order + 1):
#         Y_line = 0.0
#         for j in range(0, order + 1):
#             sum_xi_yi = 0.0
#             for k in range(len(xs)):
#                 sum_xi_yi += (xs[k] ** i * ys[k])
#             Y_line = sum_xi_yi
#         Y.append(Y_line)
#     a_matrix, A = solve_NLQ(np.array(X), Y)  # 高斯消元：求解XA=Y的A
#     # A = np.linalg.solve(np.array(X), np.array(Y))  # numpy API 求解XA=Y的A
#     error = last_square_current_loss(xs=xs, ys=ys, A=A)
#     print('最小二乘法+求解线性方程组，误差下降为：{}'.format(error))
#     return A
#
# # 可视化多项式曲线拟合结果
# def draw_fit_curve(xs, ys, A, order):
#     fig = plt.figure()
#     ax = fig.add_subplot(111)
#     fit_xs, fit_ys = np.arange(min(xs) * 0.8, max(xs) * 0.8, 0.01), []
#     for i in range(0, len(fit_xs)):
#         y = 0.0
#         for k in range(0, order + 1):
#             y += (A[k] * fit_xs[i] ** k)
#         fit_ys.append(y)
#     ax.plot(fit_xs, fit_ys, color='g', linestyle='-', marker='', label='多项式拟合曲线')
#     ax.plot(xs, ys, color='m', linestyle='', marker='.', label='曲线真实数据')
#     # plt.title(s='最小二乘法拟合多项式N={}的函数曲线f(x)'.format(order))
#     plt.legend()
#     plt.show()
# if __name__ == '__main__':
#     order = 3  # 拟合的多项式项数
#     xs, ys = init_fx_data(file)  # 曲线数据
#     # 数学解法：最小二乘法+求解线性方程组
#     A = last_square_fit_curve_Gauss(xs=xs, ys=ys, order=order)
#     print(A)
#     # 迭代解法：最小二乘法+梯度下降
#     # A = last_square_fit_curve_Gradient(xs=xs, ys=ys, order=order, iternum=10000, learn_rate=0.001)
#     draw_fit_curve(xs=xs, ys=ys, A=A, order=order)  # 可视化多项式曲线拟合结果