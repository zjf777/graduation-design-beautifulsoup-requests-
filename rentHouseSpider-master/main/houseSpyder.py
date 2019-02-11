import requests
from bs4 import BeautifulSoup
from os import path
from wordcloud import WordCloud, ImageColorGenerator
import jieba.analyse
import matplotlib.pyplot as plt
from scipy.misc import imread
import time
from pymongo import MongoClient


class HouseSpider:
    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.gzzf2 = self.client.gzzf2


    session = requests.Session()
    baseUrl = "http://gz.zu.fang.com"

    urlDir = {
        "不限": "/house/",
        "天河": "/house-a073/",
        "番禺": "/house-a078/",
        "海珠": "/house-a074/",
        "白云": "/house-a076/",
        "越秀": "/house-a072/",
        "花都": "/house-a0639/",
        "增城": "/house-a080/",
        "荔湾": "/house-a071/",
        "黄埔": "/house-a075/",
        "南沙": "/house-a084/",
        "从化": "/house-a079/",

    }
    region = "不限"
    page = 100
    # 通过名字获取 url 地址
    def getRegionUrl(self, name="天河", page=10):
        urlList = []
        for index in range(page):
            if index == 0:
                urlList.append(self.baseUrl + self.urlDir[name])
            else:
                urlList.append(self.baseUrl + self.urlDir[name] + "i3" + str(index + 1) + "/")

        return urlList



    # MongoDB 存储数据结构
    def getRentMsg(self, title, rooms, area, price, address, traffic, region, direction):
        return {
            "title": title,  # 标题
            "rooms": rooms,  # 房间数
            "area": area,  # 平方数
            "price": price,  # 价格
            "address": address,  # 地址
            "traffic": traffic,  # 交通描述
            "region": region,  # 区、（海珠、天河区）
            "direction": direction,  # 房子朝向（朝南、朝南北）
        }

    # 获取数据库 collection
    def getCollection(self, name):
        gzzf2 = self.gzzf2
        if name == "不限":
            return gzzf2.rent
        if name == "天河":
            return gzzf2.tianhe
        if name == "番禺":
            return gzzf2.panyu
        if name == "海珠":
            return gzzf2.haizhu
        if name == "白云":
            return gzzf2.baiyun
        if name == "越秀":
            return gzzf2.yuexiu
        if name == "花都":
            return gzzf2.huadu
        if name == "增城":
            return gzzf2.zengcheng
        if name == "荔湾":
            return gzzf2.liwan
        if name == "南沙":
            return gzzf2.nansha
        if name == "从化":
            return gzzf2.conghua
        if name == "黄埔":
            return gzzf2.huangpu

    #
    def getAreaList(self):
        return [
            "不限",
            "天河",
            "番禺",
            "海珠",
            "白云",
            "越秀",
            "花都",
            "增城",
            "荔湾",
            "黄埔",
            "南沙",
            "从化"
        ]
#
    def getOnePageData(self, pageUrl, reginon="不限"):
        rent = self.getCollection(self.region)
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36'})
        res = self.session.get(
            pageUrl
        )
        soup = BeautifulSoup(res.text, "html.parser")
        divs = soup.find_all("dd", attrs={"class": "info rel"})  # 获取需要爬取得 div

        for div in divs:
            ps = div.find_all("p")
            try:  # 捕获异常，因为页面中有些数据没有被填写完整，或者被插入了一条广告，则会没有相应的标签，所以会报错
                for index, p in enumerate(ps):  # 从源码中可以看出，每一条 p 标签都有我们想要的信息，故在此遍历 p 标签，
                    text = p.text.strip()
                    print(text)  # 输出看看是否为我们想要的信息
                print("===================================")
                # 爬取并存进 MongoDB 数据库
                roomMsg = ps[1].text.split("|")
                # rentMsg 这样处理是因为有些信息未填写完整，导致对象报空
                area = roomMsg[2].strip()[:len(roomMsg[2]) - 2]
                rentMsg = self.getRentMsg(
                    ps[0].text.strip(),
                    roomMsg[1].strip(),
                    int(float(area)),
                    int(ps[len(ps) - 1].text.strip()[:len(ps[len(ps) - 1].text.strip()) - 3]),
                    ps[2].text.strip(),
                    ps[3].text.strip(),
                    ps[2].text.strip()[:2],
                    roomMsg[3],
                )
                rent.insert(rentMsg)
            except:
                continue

#
    def setRegion(self, region):
        self.region = region
#
    def setPage(self, page):
        self.page = page
#
    def startSpicder(self):
        for url in self.getRegionUrl(self.region, self.page):
            self.getOnePageData(url, self.region)
            print("=================== one page 分割线 ===========================")
            print("=================== one page 分割线 ===========================")
            print("=================== one page 分割线 ===========================")
            time.sleep(2)
#
region_list = ["不限","天河","番禺","海珠","白云","越秀","花都","增城","荔湾","黄埔","南沙","从化"]
for region in region_list:
    spider = HouseSpider()
    spider.setPage(1)  # 设置爬取页数
    spider.setRegion(region)  # 设置爬取区域
    spider.startSpicder()  # 开启爬虫





