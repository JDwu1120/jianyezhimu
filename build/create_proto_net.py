# -*- coding:utf-8 -*-
import os
import sys
from sys import argv
sys.path.append('/usr/local/Cellar/caffe/python')
from caffe import layers as L,params as P,to_proto
from caffe.proto import caffe_pb2

#Usage : python create_proto_net.py path
# path = os.getcwd() #保存文件路径
train_path = 'train' #训练数据lmdb
vali_path = 'validata' #验证数据lmdb
train_bin_path = 'train.binaryproto' #均值文件位置
train_proto_path  = 'train.prototxt' #训练集配置文件
vali_proto_path = 'validata.prototxt' #验证集配置文件
solver_path='solver.prototxt'
s = caffe_pb2.SolverParameter()

def create_net(lmdb,batch_size,include_acc=False):
    #创建第一层数据层
    num = 0
    if  lmdb == vali_path:
        num = 1
    data,label=L.Data(
        source=lmdb,                             #数据源，训练数据LMDB文件的位置
        backend=P.Data.LMDB,                     #数据类型，本文是lmdb
        batch_size=batch_size,                   #batch大小
        ntop=2,                                  #输出数量，本文是data和label，所以是2
        transform_param=dict(crop_size=200,       #crop大小
                             mean_file=train_bin_path, #均值文件
                             mirror=True,         #镜像操作
                             scale = 0.00390625
                                 ),
        include=dict(
            phase = num
            )
        )
    frozen_weight_param = dict(lr_mult=1)#权重
    frozen_bias_param = dict(lr_mult=2)#偏执值
    froozen_param = [frozen_weight_param, frozen_bias_param]
    conv1=L.Convolution(
        data,                             #数据流入（即从数据层得到的data）
        kernel_size=9,                    #卷积核大小
        param = froozen_param,
        stride=1,                         #步长
        num_output=32,                    #输出
        pad=4,                            #填零
        weight_filler=dict(type='xavier'), #权重初始化方式'xavier'
        bias_filler = dict(type='constant')
    )

    relu1=L.ReLU(
        conv1,         #数据流入（即从卷积层得到的conv1）
        in_place=True  #in_place ，就地运算，节省存储开销
    )

    pool1=L.Pooling(
        relu1,               #数据流入（即从激活层得到的relu1）
        pool=P.Pooling.MAX,  #池化方式：最大池化
        kernel_size=3,       #池化核大小
        stride=2             #步长
    )
    conv2=L.Convolution(
        pool1,                             #数据流入（即从数据层得到的data）
        kernel_size=9,                    #卷积核大小
        param = froozen_param,
        stride=1,                         #步长
        num_output=32,                    #输出
        pad=4,                            #填零
        weight_filler=dict(type='xavier'), #权重初始化方式'xavier'
        bias_filler = dict(type='constant')
    )
    relu2=L.ReLU(
        conv2,         #数据流入（即从卷积层得到的conv2）
        in_place=True  #in_place ，就地运算，节省存储开销
    )

    pool2=L.Pooling(
        relu2,               #数据流入（即从激活层得到的relu2）
        pool=P.Pooling.MAX,  #池化方式：最大池化
        kernel_size=3,       #池化核大小
        stride=2             #步长
    )
    conv3=L.Convolution(
        pool2,                             #数据流入（即从数据层得到的data）
        kernel_size=9,                    #卷积核大小
        param = froozen_param,
        stride=1,                         #步长
        num_output=64,                    #输出
        pad=4,                            #填零
        weight_filler=dict(type='xavier'), #权重初始化方式'xavier'
        bias_filler = dict(type='constant')
    )
    relu3=L.ReLU(
        conv3,         #数据流入（即从卷积层得到的conv3）
        in_place=True  #in_place ，就地运算，节省存储开销
    )
    fc1=L.InnerProduct(
        relu3,                            #数据流入
        param = froozen_param,
        num_output=500,                  #全连接输出数目
        weight_filler=dict(type='xavier'), #权重初始化方式'xavier'
        bias_filler = dict(type='constant')
    )
    relu4=L.ReLU(
        fc1,         #数据流入
        in_place=True  #in_place ，就地运算，节省存储开销
    )

    fc2=L.InnerProduct(
        relu4,                            #数据流入
        num_output=100,                  #全连接输出数目
        param = froozen_param,
        weight_filler=dict(type='xavier'), #权重初始化方式'xavier'
        bias_filler = dict(type='constant')
    )

    loss = L.SoftmaxWithLoss(
        fc2,    #数据流入（即从全连接层得到的fc1）
        label   #数据流入（即从数据层得到的label）
    )

    if include_acc:                  #在训练阶段，不需要accuracy层，但是在验证阶段，是需要的
        acc = L.Accuracy(
            fc1,
            label
        )
        return to_proto(loss, acc)
    else:
        return to_proto(loss)

def write_net():
    #将以上的设置写入到prototxt文件
    with open(train_proto_path, 'w') as f:
        f.write(str(create_net(train_path,batch_size=16,)))

    with open(vali_proto_path, 'w') as f:
        f.write(str(create_net(vali_path,batch_size=16,include_acc=True)))

s.train_net = 'train.prototxt'
s.test_net.append('validata.prototxt')
s.base_lr = 0.01
s.lr_policy = 'step'

s.stepsize=2000
s.gamma = 0.1
s.max_iter = 100000

s.test_iter.append(50)
s.test_interval = 500

s.regularization_type = 'L2'
s.weight_decay = 0.0001



s.display = 100
s.snapshot = 2000
s.snapshot_prefix = 'snapshot/Leaves'
s.solver_mode = caffe_pb2.SolverParameter.CPU

def write_solver():
    #写入文件
    with open(solver_path, 'w') as f:
        f.write(str(s))

if __name__ == '__main__':
    write_net()
    write_solver()