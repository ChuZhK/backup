from collections import Counter
import numpy as np
import pandas as pd
import math

train_titanic_frame=pd.read_csv('train_titanic.csv')
train_titanic=np.array(train_titanic_frame)


'''
2) 编写函数，给定任何标记数组计算其信息熵 
输入：标记数组 
输出：该数组对应的信息熵 
计算信息熵公式: 某数组包含K个不同的取值，样本为第k(k=1,2,…,K)个值的数量所占比例为p_k,

'''
def entropy(label):
    all = np.unique(label[:])
    counter = Counter(label[:])
    ent = 0
    for n in range(len(all)):
        pk = counter[all[n]] / len(label)
        ent -= pk * math.log((pk), 2)
    return ent

'''
编写函数，函数功能为将所给的数据集按照指定维度dimension进行划分为若干个不同的数据集
 【输入】：属性集合，标记集合，维度索引 
 【输出】：划分后所得到的子树属性集合，子树标记集合
 '''

def split(feature, label, dimension):
    dim = feature[:, dimension]
    differ = np.unique(dim)  # differ为标签属性上某一维度的非重复值数组
    split_feature = []
    split_label = []
    for x in differ:
        small_feature = []
        small_label = []
        for i in range(len(dim)):
            if (x == dim[i]):
                q: list = feature[i, :]
                w: list = label[i]
                small_feature.append(q)
                small_label.append(w)
        split_feature.append(small_feature)
        split_label.append(small_label)
    return split_feature, split_label
'''
4) 编写函数，函数功能为进行【一次】决策树的结点划分
遍历找出该属性集合中信息增益(使用ID3算法中的公式计算)【最大】的属性 
输入：属性集合，标记集合 
输出：该次划分的最佳信息增益，最佳划分维度 
计算信息增益公式: 某数据集D有若干属性值以及对应的标记值，其总样本大小为|D|,
这里取其中一个属性类型feature,该特征包含V个不同的取值，
'''
def Gain(feature, label):
    best_entropy = 0
    best_dimension = 0
    for col in range(len(feature[0])):
        D = entropy(label)
        sp_feature, sp_label = split(feature, label, col)
        d_v = 0
        for arr in sp_label:
            d_v -= len(arr) / len(label) * entropy(arr)
        if d_v + D > best_entropy:
            best_entropy = d_v + D
            best_dimension = col
        col += 1
    return best_entropy, best_dimension

'''
编写函数，函数功能为进行【一次】决策树的结点划分
遍历找出该属性集合中信息增益率(使用C4.5算法中的公式计算)【最大】的属性 
输入：属性集合，标记集合 
输出：该次划分的信息增益率，最佳维度 
计算信息增益率公式: 某数据集D有若干属性值以及对应的标记值，其总样本大小为|D|
这里取其中一个属性类型feature,该属性包含V个不同的取值
'''
def getGini(label):
    differ = np.unique(label[:])
    counter = Counter(label[:])
    ent = 0
    for i in range(len(differ)):
        pk = counter[differ[i]] / len(label)
        ent += pk * pk
    return 1 - ent

def one_split_CART(feature, label):
    col = 0
    best_value = 9999
    best_dimension = 0
    best_feature = []
    for i in range(len(feature[0,:])):
        sp_feature, sp_label = split(feature, label, col)
        gini = 0
        for arr in sp_label:
            gini_part = len(arr) / len(label) * getGini(arr)
            gini += gini_part
        if gini < best_value:
            best_value = gini
            best_dimension = col
            best_feature = sp_feature
        col += 1
    return best_feature, best_dimension, best_value

'''
编写函数，进行【一次】决策树的结点划分
遍历找出该属性集合中基尼系数(使用CART算法中的公式计算)最小的属性以及最佳的划分值 
输入：属性集合，标记集合 
输出：该次划分的最佳的基尼系数，最佳维度，最佳划分值 
计算基尼系数公式: 某数据集D有若干属性值以及对应的标记值，其总样本大小为|D|
该集合中样本标记类别总共有K类，第k类样本所占比例为 (k=1,2,..,K)
'''

def one_split_C4_5(feature, label):
    best_dimension=0
    best_entropy=0
    for col in range(len(feature[0])):
        split_feature,split_label=split(feature,label,col)
        miner_ent=0
        for arr in split_label:
            miner_ent-=len(arr)/len(label)*entropy(arr)
        gain=entropy(label)+miner_ent
        Ent=entropy(feature[:,col])
        Gain_ratio=gain/Ent
        if(Gain_ratio>best_entropy):
            best_entropy=Gain_ratio
            best_dimension=col
    return best_entropy, best_dimension

if __name__=='__main__':
    feature = train_titanic[:, 0:4]
    label = train_titanic[:, 4]
    best_entroy0, best_dimension0 = Gain(feature, label)
    print("ID3方法：")
    print("最佳选取维度：", best_dimension0, "    最大信息增益", best_entroy0, )
    print("\nC4.5方法：")
    best_entroy1, best_dimension1 = one_split_C4_5(feature, label)
    print("最佳划分维度：", best_dimension1, "   最大信息增益率：", best_entroy1)
    best_entroy, best_dimension, best_value = one_split_CART(feature, label)
    print("\nCRT方法：")
    print('最佳选取维度：', best_dimension, '    最小基尼系数：', best_value)
