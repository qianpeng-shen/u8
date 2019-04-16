# encoding=utf-8
from suds.client import Client
# from phone import Phone
#
#
# a=Phone().find('16619991200')
# print(a)
# url = 'http://124.207.40.126:9000/b500/TTSWebDataAccess.asmx?WSDL'
# client = Client(url)
# print(client)
# strwhere = "where dckdate >= '2018-1-1' and dckdate<='2018-8-28' and cinvcode='1001'"
# innerMml = "92837181"
# faceName = "2018/11/30 15:34:4"
# res = client.service.GetWebData(innerMml,faceName)
# print(res)
import re
# aa = '^((13[0-9])|(14[5,7])|(15[0-3,5-9])|(17[0,3,5-8])|(18[0-9])|166|198|199|(147))\\d{8}$'
# dit = re.search(aa, '1517604933')
# if dit:
#     print("正确")
# else:
#     print("错误")
import requests
import re
import json
from multiprocessing import Pool
from multiprocessing import Manager
import time
import functools  # 函数的包装器


# 抓取猫眼TOP100的数据
# 第一步：下载页面
def get_one_page(url):
  # 设置UA
  ua_header = {
    "User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)"}
  response = requests.get(url, headers=ua_header)
  if response.status_code == 200:  # OK
    return response.text
  return None


# 第二步：提取信息
def parse_one_page(html):
  # 使用正则表达式的懒惰+findall的模式来提取信息
  pattern = re.compile(
    '<p class="name"[\s\S]*?title="([\s\S]*?)"[\s\S]*?<p class="star">([\s\S]*?)</p>[\s\S]*?<p class="releasetime">([\s\S]*?)</p>')
  items = re.findall(pattern, html)
  # 使用yield来返回信息给上层
  for item in items:
    yield {
      "title": item[0].strip(),
      "actor": item[1].strip(),
      "time": item[2].strip()
    }


# 第三步：保存到本地文件系统中
def write_to_file(item):
  # 存储成json格式，以便于将来能方便的提取出来
  with open("maoyanTop100.txt", 'a', encoding="utf-8") as f:
    f.write(json.dumps(item, ensure_ascii=False) + '\n')


# 0-100: 0,10,20,...,90
# http://maoyan.com/board/4?offset=90
def CrawlPage(lock, offset):
  # 将下载页面，解析页面及保存信息放入一个函数中
  url = "http://maoyan.com/board/4?offset=" + str(offset)
  html = get_one_page(url)
  for item in parse_one_page(html):
    lock.acquire()  # 加锁
    write_to_file(item)
    lock.release()  # 释放锁
  #    #url = "http://maoyan.com/board/4?offset="
  #    for i in range(minPage,maxPage,step):
  #        # 每次生成一个入口的URL
  time.sleep(1)


# if __name__ == "__main__":
#   # 使用进程池来抓取数据
#   # 在进程池之间通信或者加锁时需要用Manager
#   manager = Manager()
#   lock = manager.Lock()
#   # 产生一个新的包装函数
#   newCrawlPage = functools.partial(CrawlPage, lock)
#   pool = Pool()
#   pool.map(newCrawlPage, [i * 10 for i in range(10)])
#   pool.close()https://www.chahaoba.com/邯郸
#   pool.join()

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36"}
from urllib import request
print(request.urlopen( request.Request("https://www.chahaoba.com/邯郸",headers=headers)).read().decode("utf-8"))