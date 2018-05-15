# -*- coding: utf-8 -*-
import numpy as np
import cv2
import os
from os.path import dirname, join, basename
from glob import glob
from sys import argv
#本文件用来resize一个文件夹下的所有图片
#运行本脚本需要两个参数
#param1:目标文件位置
#param2:生成文件位置
#运行方法：python resize_all_img.py 目标文件路径 生成文件路径
num=0
Path = argv[1]
dir = argv[2]
file = os.listdir(Path)
dir_path = dirname(__file__)+dir
if  os.path.exists(dir_path)<>1:
    os.makedirs(dir_path)
for fn in file:
    print fn
    if  os.path.isdir(join(argv[1],fn)):
        for le in glob(join(join(argv[1],fn), '*.jpg')):
            img = cv2.imread(le)
            try:
                res=cv2.resize(img,(1000,1000),interpolation=cv2.INTER_AREA)
            except Exception as err:
                print err
            if  os.path.exists(dir_path+'/'+fn):
                img_path = dir_path+'/'+fn+'/'+str(num)+'.jpg'
                cv2.imwrite(img_path,res)
            else:
                os.makedirs(dir_path+'/'+fn)
                img_path = dir_path+'/'+fn+'/'+str(num)+'.jpg'
                cv2.imwrite(img_path,res)
            num=num+1
            print num
        for le in glob(join(join(argv[1],fn), '*.JPG')):
            img = cv2.imread(le)
            try:
                res=cv2.resize(img,(1000,1000),interpolation=cv2.INTER_AREA)
            except Exception as err:
                print err
            if  os.path.exists(dir_path+'/'+fn):
                img_path = dir_path+'/'+fn+'/'+str(num)+'.jpg'
                cv2.imwrite(img_path,res)
            else:
                os.makedirs(dir_path+'/'+fn)
                img_path = dir_path+'/'+fn+'/'+str(num)+'.jpg'
                cv2.imwrite(img_path,res)
            num=num+1
            print num
    print "one done"
print 'all done!'


