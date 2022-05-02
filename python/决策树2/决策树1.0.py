from collections import Counter
import numpy as np
import pandas as pd
import math
#计算一个标签集的信息熵
def entropy(label):
    all = np.unique(label[:])
    counter = Counter(label[:])
    ent = 0
    for a in all:
        pk = counter[a] / len(label)
        ent -= pk * math.log((pk), 2)
    return ent



#将属性集合按照dimension维度划分，返回划分后的属性集合和标签集和
def split(feature, label, dimension):
    dim = feature[:, dimension]    #取出属性集中被划分的维度
    differ = np.unique(dim)        # differ为被划分属性上某一维度的非重复值数组
    split_feature = []             #创建一个列表存储被划分的数据集
    split_label = []               #创建一个列表存储被划分后的标签集
    #遍历dimension维度上的非重复值
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


def best_split(D, A):
    label:list=D[:,len(D[0,:])-1]
    # feature=D[:,0:len(D)]
    best_entropy = -1
    best_dimension = 0
    # print("in best_split:",A)
    # if len(A)==1:
    #     return A[0]
    for col in A:
        d= entropy(label)
        sp_feature, sp_label = split(D, label, col)
        d_v=0
        i=0
        for arr in sp_label:
            d_v -= len(arr) / len(label) * entropy(sp_label[i])
            i+=1
        if d_v + d > best_entropy:
            best_entropy = d_v + d
            best_dimension = col
    return best_dimension


# 树结点类
class Node:
    def __init__(self, isLeaf=True, label=-1, index=-1):
        self.isLeaf = isLeaf  # isLeaf表示该结点是否是叶结点
        self.label = label  # label表示该叶结点的label（当结点为叶结点时有用）
        self.index = index  # index表示该分支结点的划分属性的序号（当结点为分支结点时有用）
        self.children = {}  # children表示该结点的所有孩子结点，dict类型，方便进行决策树的搜索

    def addNode(self, val, node):
        self.children[val] = node  # 为当前结点增加一个划分属性的值为val的孩子结点
        self.isLeaf = False
# 决策树类
class DTree:
    def __init__(self):
        self.tree_root = None  # 决策树的根结点
        self.possible_value = {}  # 用于存储每个属性可能的取值

    '''
    TreeGenerate函数用于递归构建决策树，伪代码参照课件中的“Algorithm 1 决策树学习基本算法”
    '''

    def TreeGenerate(self, D1, A):
        D=np.array(D1)
        # 生成结点 node
        node = Node()
        #取出最后一列作为标签集合
        label:list = D[:,len(D[0, :]) - 1]
        label_arr = np.array(label)
        if (1 == len(np.unique(label_arr[:]))):
            node.label = np.unique(label_arr)[0]
            node.isLeaf=True
            return node
        label_mark = -1    #D中样本数量最多的标签类
        Flag = True #当按照A中所存的维度进行索引属性值的时候，所有索引出来的属性值相同时flag的值为true
        for i in A:
            col=D[:,i]
            col_differ=np.unique(col)
            if len(col_differ)>1:
                Flag=False
        MAX = -1
        differ_label = np.unique(label[:])
        counter = Counter(label[:])
        for l in differ_label:
            num = counter[l]
            if (num > MAX):
                MAX = num
                label_mark = l
        if (len(A) == 0 or Flag):
            node.label = label_mark
            node.isLeaf=True
            return node
        a_star = best_split(D, A)
        node.index=a_star
        a_dimension = D[:, a_star]
        a_strat_differ=self.possible_value[a_star]
        for d in a_strat_differ:
            lis: list = []
            for i in range(len(D[:, 0])):
                if (a_dimension[i] == d):
                    tem:list=D[i,:]
                    lis.append(tem)
            if len(lis)==0:
                new_nd=Node()
                new_nd.isLeaf=True
                new_nd.label=label_mark
                node.addNode(d,new_nd)
            else:
                B: list = []
                for x in A:
                    if x == a_star:
                        continue
                    else:
                        B.append(x)
                new_node: Node = self.TreeGenerate(lis,B)
                node.addNode(d, new_node)
        return node

    '''
    train函数可以做一些数据预处理（比如Dataframe到numpy矩阵的转换，提取属性集等），并调用TreeGenerate函数来递归地生成决策树
    '''

    def train(self, D):
        D = np.array(D)  # 将Dataframe对象转换为numpy矩阵（也可以不转，自行决定做法）
        # A = set(range(D.shape[1] - 1)) # 属性集A
        A: list = list(range(len(D[0, :]) - 1))
        # 记下每个属性可能的取值
        # A = np.array(A)
        for every in A:
            E: list = D[:, every]
            self.possible_value[every] = np.unique(E)
        self.tree_root = self.TreeGenerate(D, A)  # 递归地生成决策树，并将决策树的根结点赋值给self.tree_root

        pass

    '''
    predict函数对测试集D进行预测， 并输出预测准确率（预测正确的个数 / 总数据数量）
    '''

    def search(self, node: Node, arr):
        if node.isLeaf:
            return node.label
        else:
            x = arr[node.index]
            next1 = node.children[x]
            return self.search(next1, arr)

    def predict(self, D):
        # 将Dataframe对象转换为numpy矩阵（也可以不转，自行决定做法）
        pre = []
        correct = 0
        for i in range(len(D[:, 0])):
            row = D[i, :]
            predict = self.search(self.tree_root, row)
            if predict == row[len(D[0,:]) - 1]:
                correct += 1
            pre.append(predict)
        return (correct) / len(D[:, len(D[0,:]) - 1])

        # 对于D中的每一行数据d，从当前结点x=self.tree_root开始，当当前结点x为分支结点时，
        # 则搜索x的划分属性为该行数据相应的属性值的孩子结点（即x=x.children[d[x.index]]），不断重复，
        # 直至搜索到叶结点，该叶结点的label就是数据d的预测label
        pass

if __name__=='__main__':
    train_frame = pd.read_csv('train_titanic.csv')
    dt = DTree()
    # 构建决策树
    train = np.array(train_frame)
    dt.train(train)
    # 利用构建好的决策树对测试数据集进行预测，输出预测准确率（预测正确的个数 / 总数据数量）
    test_frame = pd.read_csv('test_titanic.csv')
    test = np.array(test_frame)
    s = dt.predict(test)
    print(s)

