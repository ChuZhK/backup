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
                # print("x:\n",x)
                # print("total:\n",total[r][0])
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
    print((vals[0] + vals[1]) / vals.sum())

    vecs_T = vecs.T
    c = [(vals[i], vecs[i]) for i in range(len(vals))]
    c = sorted(c)
    c.reverse()  # 按降序排列的特征值和特征向量
    p = []
    p.append(c[0][1])
    p.append(c[1][1])
    p = (np.array(p)).T
    # print(p.shape)
    Z = p.T.dot(X)
    # print(Z.shape)
    Z_T = Z.T
    # COV2 = np.cov(Z)
    # m = Z.dot(Z_T)
    # print("Z_T:\n", Z_T.dot(Z))

    ########################################################################以下为聚类
    k = 3  # 聚类的簇数

    # 在降维后的数据集中随机选取k列数据
    # i_k = 0
    # 样本中心集合
    # K = []
    col_rand = np.arange(Z.shape[1])
    np.random.shuffle(col_rand)
    col = Z[:, col_rand[0:k]]
    col = np.array(col).T
    total=[]
    for co in range(len(col)):
        tem=[col[co],[]]
        total.append(tem)

    # list1 = []
    # list2 = []
    # list3 = []
    # total = [[col[0], list1], [col[1], list2], [col[2], list3]]
    flag=True
    while flag:
        flag=False
        total,flag=k_means(total,Z_T,k,flag)



    for ca in total:
        print(np.array(ca[1]).reshape(-1,2))
        plt.scatter(np.array(ca[1]).reshape(-1,2)[:,0],np.array(ca[1]).reshape(-1,2)[:,1])
    plt.show()

    # node = [[], [], []]
    # # print(type(Z[:,0].tolist()))
    # # print(type(col[:,0]))
    # total_num = 0
    # while total_num < 100:
    #     total[0][1] = total[1][1] = total[2][1] = []
    #     for g in range(len(Z_T[:, 0])):  # 遍历降维后数据集
    #         distance = -1
    #         max_t: list = []
    #         for e in total:  # 与k个样本中心点逐个比较
    #             if distance == -1:
    #                 distance = dis(e[0], Z_T[g, :])
    #                 max_t = e
    #             elif dis(e[0], Z_T[g, :]) < distance:
    #                 distance = dis(e[0], Z_T[g, :])
    #                 max_t = e
    #         max_t[1].append(Z_T[g])
    #     for i in range(len(total)):
    #         node[i] = total[i][1] = (np.array(total[i][1]).reshape(-1, 2)).tolist()
    #         total[i][0] = np.average(np.array(total[i][1]), axis=0)
    #     total_num += 1
    # new_array = np.array(total[0][1])
    # x5=np.array(new_array[:,0])
    # y5=np.array(new_array[:,1])
    # plt.scatter(x5, y5)
    # plt.show()
    # print(123)


