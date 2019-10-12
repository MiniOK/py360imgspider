from retrying import retry
import requests
import urllib.request
import json
import time
import argparse
import os


# 创建Img 类
class Img:
    def __init__(self, target, total, imgs):
        """
        爬虫基本形式，有起始 url，模拟浏览器需要请求头封装header
        :param target: spider imges type
        :param total: spider imges amount
        :param imgs: spdier imges store
        """
        self.imgs = imgs
        self.total = total
        self.temp_url = "https://image.so.com/zjl?ch={0}&sn={1}&listtype=new&temp=1".format(target, None)

        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36",
            "Referer": "http://s.360.cn/0kee/a.html", "Connection": "keep-alive"}
        self.num = 1

    def get_img_list(self, url):
        """
        :param url: 封装好的完整的 url ，作为请求的url
        :return:将从 json中解析出来的 图片路径封装成 list 返回
        """
        response = requests.get(url, headers=self.headers)
        html_str = response.content.decode()
        json_str = json.loads(html_str)
        img_str_list = json_str["list"]
        img_list = []
        for img_object in img_str_list:
            img_list.append(img_object["qhimg_url"])
        return img_list

    def save_img_list(self, img_list):
        """
        :param img_list: 图片路径的list
        :return:
        """
        for img in img_list:
            self.save_img(img)

    @retry(stop_max_attempt_number=3)
    def save_img(self, img):
        """
        对获取的 图片url进行下载 保存到本地
        当保存图片出现异常的时候  就需要用retry   进行回滚  , 再次 保存当前图片 stop_max_attempt_number重试的次数
        :param img: 图片下载路径
        :return:
        """
        # 创建本地存储图片的目录
        path = "..\\..\\img_data\\{}\\".format(str(self.imgs))
        if not os.path.exists(path):
            os.mkdir(path)

        with open("{}".format(path) + str(self.num) + ".jpg", "wb") as f:
            f.write((urllib.request.urlopen(img)).read())
            print(str(self.num) + "保存成功")
            self.num += 1

    def run(self):
        """
        实现主要逻辑
        :return:
        """
        while True:
            # 1获取链接
            url = self.temp_url.format(self.num)
            # 获取数据
            img_list = self.get_img_list(url)
            # 保存数据
            self.save_img_list(img_list)
            if self.num >= int(self.total):
                print("下载完成！")
                break
            else:
                # 不要获取数据过于频繁
                print("------ 休息  5  秒------")
                time.sleep(5)


if __name__ == '__main__':

    # 360图片类别 （美女 图解电影  壁纸  设计  搞笑  图说世界  艺术  汽车  摄影  没事  家居  萌宠）
    target_list = ["beauty", "video", "wallpaper", "design", "food", "funny", "news", "art", "car", "photograpy", "home", "pet"]

    # 一个网页有30条数据 以 30 为单位  起步30
    total_list = [30, 60, 90, 120, 150, 180]

    # python 命令行解析器 argparse
    parser = argparse.ArgumentParser(description="360图片类别:（美女 图解电影  壁纸  设计  搞笑  图说世界  艺术  汽车  摄影  没事  家居  萌宠）")
    parser.add_argument("imges_type")
    parser.add_argument("num", type=int)
    parser.add_argument("imgs")
    args = parser.parse_args()

    kw = {
        "target": args.imges_type,  # 爬取图片类别
        "total": args.num,  # 爬取条数
        "imgs": args.imgs,  # 本地存放图片的位置，自动创建
    }
    # 启动爬虫
    img = Img(**kw)
    img.run()

    """
         注意：
         在命令行命令示例；
         $: python py360imgspider.py [图片类型] [数量(以30为单元)] [存储地址（自定义一个目录：例如 car_imgs，就会爬py360imgspider.py文件同级创建一个目录）]
         $: python py360imgspider.py car 30 car_imgs
    """
