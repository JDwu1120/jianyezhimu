# -*- coding:utf-8 -*-
from sys import argv
import os

#本脚本的目的是将测试图片集写入txt文件中以便caffe的使用
#两个参数：path 目标文件
#         direction 写入文件


def find_all_dir(path,direction):
    if  os.path.isdir(path)==0:
        with open(os.getcwd()+'/'+direction,'a') as f:
            f.write(path+'\n')
        return
    dir = os.listdir(path)
    for di in dir:
        find_all_dir(path+'/'+di,direction)
def  main():
    path = argv[1]
    direction = argv[2]
    if len(argv) <> 3:
        print "Usage:python test_to_test.py path direction"
    find_all_dir(path,direction)
if __name__ == '__main__':
    main()