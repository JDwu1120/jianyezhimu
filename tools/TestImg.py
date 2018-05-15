# encoding=utf-8
import sys
import json
from sys import argv
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


def main():
    mean_file = 'CNN_TRAINDATA/train.npy'
    mean = np.load(mean_file)  # 加载均值文件
    classifier = Classfier('prototxt/deploy.prototxt', 'snapshot/Leaves_iter_10000.caffemodel', mean)  # 创建我们的分类器
    name = argv[1]
    name = name.strip()
    img = cv2.imread(name)  # 读取图片
    img=cv2.resize(img,(500,500),interpolation=cv2.INTER_AREA)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    prob = classifier.classify(img)  # 使用分类器分类，得到概率
    print prob
    sort = np.argsort(-prob)
    print np.argmax(prob) # 输出概率最大值对应的英文字母
    res = []
    for i in range(0,5,1):
        # res.append(prob[0][sort[0][i]])
        res.append({
            'id':sort[0][i],
            'rate': str(prob[0][sort[0][i]])
        })
    ret = {'code':1,
           'msg':'adads',
           'data':res
           }
    # ret = json.dumps(ret)
    print json.dumps(ret)
    # print dict
if __name__ == '__main__':
    main()
