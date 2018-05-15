#!/bin/bash
#将预先分类好的图片resize
python build/resize_all_img.py leaves class_resize

#对resize好的图片进行训练集和验证集的分类并且记录对应的字典
python build/class_to_txt.py class_resize pic

#将训练集的txt和验证集的txt转换成caffe可以识别的lmdb文件
convert_imageset --check_size -shuffle ./ train.txt train
convert_imageset --check_size -shuffle ./ validata.txt validata

#计算图片的均值
compute_image_mean train train.binaryproto

#将均值文件转换成npy文件
python build/bin2npy.py train.binaryproto train.npy

#生成训练网络和解决网络
#python build/create_proto_net.py

#创建快照
mkdir snapshot

#训练模型
caffe train -solver solver.prototxt
