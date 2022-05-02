from collections import Counter
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math

train_titanic_frame = pd.read_csv('train_titanic.csv')
train_titanic = np.array(train_titanic_frame)


def entropy(label):
    all = np.unique(label[:])
    counter = Counter(label[:])
    ent = 0
    for n in range(len(all)):
        pk = counter[all[n]] / len(label)
        ent -= pk * math.log((pk), 2)
    return ent


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
#
# class Node:
#     def __init__(self):
#         self.domension=None
#         self.left=None
#         self.right=None
#         self.label=None
#         return
#
#     def setdim(self,col):
#         self.domension=col
#         return
#
#     def setleft(self,node):
#         self.left=node
#         return
#
#
#     def setright(self,node):
#         self.right=node
#         return
#
#     def setlabel(self,lab):
#         self.label=lab
#         return
#
# class Tree:
#     def __init__(self,node:object):
#         self.root=node
#         self.left=None
#         self.right=None
#         self.dimension=None
#         return
#
#     def setleft(self,node:object):
#         self.left=node
#         return
#
#     def setright(self,node:object):
#         self.right=node
#         return

if __name__ == '__main__':
    feature = train_titanic[:, 0:4]
    label = train_titanic[:, 4]
    best_entroy0, best_dimension0 = Gain(feature, label)
    print("最佳选取维度：", best_dimension0,"    最大信息增益",best_entroy0, )
    best_entroy, best_dimension,best_value=one_split_CART(feature, label)
    print('\n最佳选取维度：',best_dimension,'    最小基尼系数：',best_value)
    best_entroy1,best_dimension1=one_split_C4_5(feature,label)
    print("\n最佳划分维度：",best_dimension1,"   最大信息增益率：",best_entroy1)