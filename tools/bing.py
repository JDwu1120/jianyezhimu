#! usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  7 10:56:13 2017
CSDN对应文章连接
http://blog.csdn.net/Hk_john/article/details/78455889
@author: HK
"""
import urllib.error
import time
import os
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

# 从得到的图片链接下载图片，并保存
f = open('out.txt', 'w', encoding='utf-8')


def SaveImage(link, InputData, count):
    try:
        time.sleep(0.2)
        urllib.request.urlretrieve(link, './' + InputData + '/' + str(count) + '.jpg')
    except urllib.error.HTTPError as urllib_err:
        print(urllib_err)
    except Exception as err:
        time.sleep(1)
        print(err)
        print("产生未知错误，放弃保存")
    else:
        print("图+1,已有" + str(count) + "张图")


# 找到图片的链接
def FindLink(PageNum, InputData, word):
    for i in range(PageNum):
        print(i)
        try:
            url = 'http://cn.bing.com/images/async?q={0}&first={1}&count=35&relp=35&lostate=r&mmasync=1&dgState=x*175_y*848_h*199_c*1_i*106_r*0'
            agent = {
                'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.165063 Safari/537.36 AppEngine-Google."}
            page1 = urllib.request.Request(url.format(InputData, i * 35 + 1), headers=agent)
            page = urllib.request.urlopen(page1)
            soup = BeautifulSoup(page.read(), 'html.parser')
            print(type(soup))
            # print(soup, file == f)
            # print(soup.decode('utf-8'))
            if not os.path.exists("./" + word):
                os.mkdir('./' + word)

            for StepOne in soup.select('.mimg'):
                print(type(StepOne))
                link = StepOne.attrs['src']
                count = len(os.listdir('./' + word)) + 1
                SaveImage(link, word, count)
        except Exception as err:
            print(err)
            print('URL OPENING ERROR !')


if __name__ == '__main__':
    # 输入需要加载的页数，每页35幅图像
    PageNum = 5
    # 输入需要搜索的关键字
    words = ['Acer_Campestre', 'Acer_Capillipes', 'Acer_Circinatum', 'Acer_Mono', 'Acer_Opalus', 'Acer_Palmatum',
             'Acer_Pictum', 'Acer_Platanoids', 'Acer_Rubrum', 'Acer_Rufinerve', 'Acer_Saccharinum', 'Alnus_Cordata',
             'Alnus_Maximowiczii', 'Alnus_Rubra', 'Alnus_Sieboldiana', 'Alnus_Viridis', 'Arundinaria_Simonii',
             'Betula_Austrosinensis', 'Betula_Pendula', 'Callicarpa_Bodinieri', 'Castanea_Sativa', 'Celtis_Koraiensis',
             'Cercis_Siliquastrum', 'Cornus_Chinensis', 'Cornus_Controversa', 'Cornus_Macrophylla', 'Cotinus_Coggygria',
             'Crataegus_Monogyna', 'Cytisus_Battandieri', 'Eucalyptus_Glaucescens', 'Eucalyptus_Neglecta',
             'Eucalyptus_Urnigera', 'Fagus_Sylvatica', 'Ginkgo_Biloba', 'Ilex_Aquifolium', 'Ilex_Cornuta',
             'Liquidambar_Styraciflua', 'Liriodendron_Tulipifera', 'Lithocarpus_Cleistocarpus', 'Lithocarpus_Edulis',
             'Magnolia_Heptapeta', 'Magnolia_Salicifolia', 'Morus_Nigra', 'Olea_Europaea', 'Phildelphus',
             'Populus_Adenopoda', 'Populus_Grandidentata', 'Populus_Nigra', 'Prunus_Avium', 'Prunus_X_Shmittii',
             'Pterocarya_Stenoptera', 'Quercus_Afares', 'Quercus_Agrifolia', 'Quercus_Alnifolia', 'Quercus_Brantii',
             'Quercus_Canariensis']
    words = sorted(words, reverse=True)
    for word in words:
        InputData = urllib.parse.quote(word)
        FindLink(PageNum, InputData, word)

