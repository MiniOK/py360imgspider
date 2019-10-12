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
