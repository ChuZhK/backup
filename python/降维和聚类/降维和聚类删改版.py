import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import random
import statistics
import matplotlib as mpl
from pandas.core.frame import DataFrame
import warnings

warnings.filterwarnings('ignore')
train_data_frame = pd.read_csv('train_data.csv')
train = np.array(train_data_frame)
X = train.T
X = X.reshape(9, 167)


# 计算欧氏距离
def dis(x, y):
    sum = 0
    for i in range(len(x)):
        sum += (x[i] - y[i]) * (x[i] - y[i])
    sum = math.pow(sum, 0.5)
    return sum

#迭代一次的函数
def k_means(total,data,k,flag):
    new_total=[]
    for i in total:
        tem_list=[[],[]]
        new_total.append(tem_list)
    for x in data:
        distance=-1
        node_rank=0
        for r in range(k):
            if distance==-1:
                distance=dis(x,total[r][0])
                node_rank=r
            elif dis(x,total[r][0])<distance:
                distance=dis(x,total[r][0])
                node_rank=r
        new_total[node_rank][1].append(x)
    xm=0
    for m in new_total:
        m[0]=np.average(m[1],axis=0)
    for k in range(len(total)):
        if np.average(total[k][1],axis=0).all()!=np.average(new_total[k][1],axis=0).all():
            flag=True
            break
    return new_total,flag



# 打印结果
if __name__ == '__main__':
    aver_X = np.average(X, axis=1)
    aver_X = aver_X.reshape(9, 1)
    X = X - aver_X
    COV = X.dot(X.T) / 176
    vals, vecs = np.linalg.eig(COV)
    # print("该矩阵的特征值:", vals)
    # print("该矩阵的特征向量:\n", vecs)
    vecs_T = vecs.T
    c = [(vals[i], vecs[i]) for i in range(len(vals))]
    c = sorted(c)
    c.reverse()  # 按降序排列的特征值和特征向量
    p = []
    p.append(c[0][1])
    p.append(c[1][1])
    p = (np.array(p)).T
    Z = p.T.dot(X)
    Z_T = Z.T
    ########################################################################以下为聚类
    k = 5  # 聚类的簇数
    col_rand = np.arange(Z.shape[1])
    np.random.shuffle(col_rand)
    col = Z[:, col_rand[0:k]]
    col = np.array(col).T
    total=[]
    for co in range(len(col)):
        tem=[col[co],[]]
        total.append(tem)
    flag = True
    while flag:
        flag=False
        total,flag=k_means(total,Z_T,k,flag)
    for ca in total:
        print(np.array(ca[1]).reshape(-1,2))
        plt.scatter(np.array(ca[1]).reshape(-1,2)[:,0],np.array(ca[1]).reshape(-1,2)[:,1])
    plt.show()




