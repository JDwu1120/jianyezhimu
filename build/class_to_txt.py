# -*- coding:utf-8 -*-
import os
import imghdr
import cv2
from sys import argv
#本脚本目的是为了将图片的类型分为训练集和验证集合
#将图片对应的种类写入到txt文件中以适应caffe
#同时建立种类对照表
#本脚本接受两个个参数path和direction
#path：为目标文件目录
#direction：为图片储存路径
path  = argv[1]
direction = argv[2]
if os.path.isdir(path):
    list = os.listdir(path)
    #树叶的种类
    num = 0
    for li in list:
        #li是每种树叶的类别
        if li == '.DS_Store':
            continue
        new_path = os.getcwd()+'/'+path+'/'+li
        if os.path.isdir(new_path):
            li_1 = os.listdir(new_path)
            length = len(li_1)-1
            #创建目录
            if os.path.exists(os.getcwd()+'/'+direction)==0:
                os.makedirs(os.getcwd()+'/'+direction)
            id = 0
            #每一类图片的list
            for img in li_1:
                src = os.getcwd()+'/'+path+'/'+li+'/'+img
                img_path = direction+'/'+img
                dir_path = os.getcwd()+'/'+direction+'/'+img
                type = imghdr.what(src)
                if type <> 'jpeg' and type <> 'png':
                    print type
                    continue
                if id < 3*length/4:
                    # print os.getcwd()+'/'+'class_resize/'+li+'/'+img+' '+li
                    with open(os.getcwd()+'/'+'train.txt','a') as f:
                        f.write(img_path+' '+str(num)+'\n')
                    cv_img = cv2.imread(src)
                    cv2.imwrite(dir_path,cv_img)
                else:
                    # print "Haha"
                    with open(os.getcwd()+'/'+'validata.txt','a') as f:
                        f.write(img_path+' '+str(num)+'\n')
                    cv_img = cv2.imread(src)
                    cv2.imwrite(dir_path,cv_img)
                id = id+1
            with open(os.getcwd()+'/'+'dictionary.txt','a') as f:
                f.write(str(num)+' '+li+'\n')
        num += 1
print 'all done'