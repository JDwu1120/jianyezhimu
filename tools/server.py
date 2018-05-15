# -*- coding=utf-8 -*-


"""
file: recv.py
socket service
"""


import socket
import json
import threading
import os
import struct
import sys
import imghdr
sys.path.append('/usr/local/Cellar/caffe/python')  # 先将pycaffe 路径加入环境变量中
import caffe, cv2, numpy as np

class Classfier:  # 将模型封装入一个分类器类中
    def __init__(self, deploy, model, mu):
        self.net = caffe.Net(deploy, model, caffe.TEST)  # 初始化网络结构及其中的参数
        self.mu = mu

    def classify(self, img):
        img = (img - self.mu) * 0.00390625  # 减去均值后再进行缩放
        self.net.blobs['data'].data[...] = img  # 将图片数据送入data层的blobs
        out = self.net.forward()['prob']  # 执行前向计算，并得到最后prob层的输出结果
        return out
mean_file = 'train.npy'
mean = np.load(mean_file)  # 加载均值文件
classifier = Classfier('deploy.prototxt', 'snapshot/alpha_iter_10000.caffemodel', mean)  # 创建我们的分类器

def socket_service():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('0.0.0.0', 6666))
        s.listen(10)
    except socket.error as msg:
        print msg
        sys.exit(1)
    print 'Waiting connection...'

    while 1:
        conn, addr = s.accept()
        t = threading.Thread(target=deal_data, args=(conn, addr))
        t.start()

def deal_data(conn, addr):
    print 'Accept new connection from {0}'.format(addr)
    conn.settimeout(500)
    # conn.send('Hi, Welcome to the server!')

    while 1:
        fileinfo_size = struct.calcsize('128sl') #文件传输包struct
        buf = conn.recv(fileinfo_size)
        if buf:
            filename, filesize = struct.unpack('128sl', buf)
            fn = filename.strip('\00')
            new_filename = os.path.join('user/', 'new_' + fn)
            print 'file new name is {0}, filesize if {1}'.format(new_filename,
                                                                 filesize)

            recvd_size = 0  # 定义已接收文件的大小
            fp = open(new_filename, 'wb')
            print 'start receiving...'

            while not recvd_size == filesize:
                if filesize - recvd_size > 1024:
                    data = conn.recv(1024)
                    recvd_size += len(data)
                else:
                    data = conn.recv(filesize - recvd_size)
                    recvd_size = filesize
                fp.write(data)
            fp.close()
            img = new_filename
            img = img.strip()
            type = imghdr.what(img)
            if type <> 'jpeg' and type <> 'png':
                continue
            try:
                img = cv2.imread(img)  # 读取图片
                img=cv2.resize(img,(1000,1000),interpolation=cv2.INTER_AREA)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            except Exception,e:
                ret = {'code':1,
                       'msg':'fail',
                       'data':[]
                       }
                # conn.sendall(bytes(np.argmax(prob))) #返回预测图片的种类
                conn.sendall(bytes(json.dumps(ret)))
            prob = classifier.classify(img)  # 使用分类器分类，得到概率
            # print np.argmax(prob) # 输出概率最大值对应的英文字母
            sort = np.argsort(-prob)
            #将返回的数据以json的格式传输到client
            #格式
            # {
            #     "msg": "adads",
            #     "code": 1,
            #     "data": [
            #         {
            #             "id": 72,
            #             "rate": 23.45
            #         },
            #         {
            #             "id": 72,
            #             "rate": 23.45
            #         },
            #         {
            #             "id": 72,
            #             "rate": 23.45
            #         }
            #     ]
            # }
            res = []
            for i in range(0,5,1):
                res.append({
                    'id':sort[0][i],
                    'rate': str(prob[0][sort[0][i]])
                })
            ret = {'code':0,
                    'msg':'success',
                    'data':res
                  }
            # conn.sendall(bytes(np.argmax(prob))) #返回预测图片的种类
            conn.sendall(bytes(json.dumps(ret)))
            print 'end receive...'
        conn.close()
        break


if __name__ == '__main__':
    socket_service()