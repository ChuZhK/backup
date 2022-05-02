import numpy as np
import pandas as pd
import time


if __name__=='__main__':
    train_frame = pd.read_csv('train2.csv')
    train = np.array(train_frame)
    #设置学习率
    eta=0.05
    #提取X矩阵和标签矩阵
    x = train[:,0:3]
    label=train[:,3]
    #将标签矩阵重整确保秩为1
    label=label.reshape(-1,1)
    #创建一个系数矩阵并初始化系数为0
    W=np.zeros((3,1))
    b=0
    i=0
    #输出计算时间
    k=time.time()
    #梯度下降迭代
    while i<10000:
       w0=np.sum(train[:,0].reshape(-1,1)*((x.dot(W)+b)-label))/len(label)*eta
       w1=np.sum(train[:,1].reshape(-1,1)*((x.dot(W)+b)-label))/len(label)*eta
       w2=np.sum(train[:,2].reshape(-1,1)*((x.dot(W)+b)-label))/len(label)*eta
       b=np.sum((x.dot(W)+b-label))/len(label)*eta
       W[0,0]-=w0
       W[1,0]-=w1
       W[2,0]-=w2
       i+=1
    print("计算模型用时：",time.time()-k)
    print(W,b)
    test_frame=pd.read_csv('test2.csv')
    test=np.array(test_frame)
    Test=test[:,0:3]
    pre_out=Test.dot(W)
    # print(pre_out)
    #计算MSE
    mse=0
    for i in range(len(pre_out)):
        mse+=(pre_out[i,0]+b-test[i,3])*(pre_out[i,0]+b-test[i,3])
    print("均方误差为：",mse/len(pre_out))