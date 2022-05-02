import pandas as pd
import numpy as np
import  warnings
import math
def fun(x):
    return (1-1/(1+math.exp(x)))

if __name__=='__main__':
    warnings.filterwarnings('ignore')
    train_frame = pd.read_csv('flower_train.csv')
    train_frame[['x1','x2']]=\
    train_frame[['x1','x2']].replace(0,np.NaN)
    temp_x1 = train_frame[train_frame['x1'].notnull()]
    temp_x1 = temp_x1[['x1', 'type']].groupby(['type'])[['x1']].mean().reset_index()

    # 使用dataframe的loc函数将指定条件的x1列和type列筛选出来进行值替换操作
    train_frame.loc[(train_frame['type'] == 'Iris-setosa') & (train_frame['x1'].isnull()), 'x1'] = temp_x1['x1'][0]
    train_frame.loc[(train_frame['type'] == 'Iris-versicolor') & (train_frame['x1'].isnull()), 'x1'] = temp_x1['x1'][
        1]

    # 先对x2列进行分离，之后将type按照性别进行分类，之后使用mean函数分别计算Iris-setosa和Iris-versicolor非空数据的x1的平均值
    temp_x2 = train_frame[train_frame['x2'].notnull()]
    temp_x2 = temp_x2[['x2', 'type']].groupby(['type'])[['x2']].mean().reset_index()

    # 使用dataframe的loc函数将指定条件的x1列和type列筛选出来进行值替换操作
    train_frame.loc[(train_frame['type'] == 'Iris-setosa') & (train_frame['x2'].isnull()), 'x2'] = temp_x2['x2'][0]
    train_frame.loc[(train_frame['type'] == 'Iris-versicolor') & (train_frame['x2'].isnull()), 'x2'] = temp_x2['x2'][
        1]
    # print(train1_frame)

    train_frame['type'] = np.where(train_frame['type'] == "Iris-setosa", 0, 1)
    train=np.array(train_frame)
    data=train[:,0:2]
    W=np.zeros((2,1))
    data=data.dot(W)
    b=0
    eta=0.05
    i=0
    print(fun(data+b))
    while i<10:
        e_data=fun(data+b)



