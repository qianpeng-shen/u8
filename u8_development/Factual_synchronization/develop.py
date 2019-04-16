# encoding=utf-8
import json
import queue
import re
import threading
import logging
import time
import datetime

from urllib import request

from resolve import Data
from logger import loger

#创建两个队列
url_queue = queue.Queue()
data_queue = queue.Queue()

# 获取u8token信息
class Token():

    def __init__(self):
        self.content_type = 'text/html'
        self.charset = 'utf-8'

    def run(self):
        url = 'https://api.yonyouup.com/system/token?from_account=bolebaokaifa&app_key=opa87ad77a2a44f12df&app_secret=7027dd0c880141308bedc8bfd0b854c9'
        request_obj = request.Request(url)
        request_obj.add_header('Content-Type', self.content_type)
        request_obj.add_header('charset', self.charset)

        json_data = request.urlopen(request_obj).read().decode()
        result = json.loads(json_data)
        if len(result) > 0:
            # print('token为：', result['token']['id'])
            return result['token']['id']
        else:
            errcode = result['errcode']
            errmsg = result['errmsg']
            loger().error('获取token异常,异常码为%s，异常信息为%s' % (errcode, errmsg))

token = Token().run()

# 线程类， 执行请求u8接口
class ThreadYongYout(threading.Thread):

    def __init__(self, url_queue):
        threading.Thread.__init__(self)
        self.url_queue = url_queue

    def request(self, url):
        dict = {}
        obj = re.findall(r'\w+', url)[5]

        content_type = 'text/html'
        charset = 'utf-8'

        request_obj = request.Request(url)
        request_obj.add_header('Content-Type', content_type)
        request_obj.add_header('charset', charset)

        json_data = request.urlopen(request_obj).read().decode()
        result = json.loads(json_data)
        if result :
            if result['errcode'] == '0':

                dict[obj] = result
                return dict

            elif result['errcode'] == '30012':

                old_token = url.split('&')[3].split('=')[1]
                token = Token().run()
                old_token = 'token=' + old_token
                new_token = 'token=' + token
                url = re.sub(old_token, new_token, url)
                ThreadYongYout.request(self, url)

            elif result['errcode'] == '20006':

                logging.info(result,'有错误，错误的url为：',url)
                return "error"
            elif result['errcode'] == '20002':

                return 'finish'

            else:
                logging.info(result,url)
                return "error"
        else:
            return None

    def run(self):
        while True:
            url = self.url_queue.get()
            old_token = url.split('&')[3].split('=')[1]
            old_token = 'token=' + old_token
            new_token = 'token=' + token
            url = re.sub(old_token, new_token, url)
            try:
                result = ThreadYongYout.request(self, url)

                if len(result) == None:
                    i = 1
                    while i < 3:
                        result = ThreadYongYout.request(self, url)
                        if len(result) == None:
                            print("出错")
                        else:
                            data_queue.put(result)
                            break
                        i += 1
                elif result == "error":
                    continue
                elif result == "finish":

                    self.url_queue.task_done()
                    break

                else:
                    data_queue.put(result)
                    (key, value), = result.items()

                    pagenum_data = re.findall(r'page_index=\d+', url)[0]
                    pagenum = pagenum_data.split('=')[1]
                    #当第一次做请求时，将此url循环的递增到最后
                    if int(pagenum) == 1:
                        page = 2
                        page_cont = value['page_count']

                        while page <= int(page_cont):
                            pages = 'page_index=' + str(page)
                            url_list = url.split('page_index=1')

                            next_url = url_list[0] + pages + url_list[1]
                            url_queue.put(next_url)
                            page += 1
            except Exception as error:
                loger().error(error)
            self.url_queue.task_done()

#  处理data_queue的数据
class ThreadData(threading.Thread):

    def __init__(self, data_queue):
        threading.Thread.__init__(self)
        self.data_queue = data_queue

    def run(self):

        while True:
            data = self.data_queue.get()
            (key, value), = data.items()

            if key == 'customer':# 购买渠道

                Data(value).customer()

            elif key == 'saleorderlist':  # 订单信息

                Data(value).saleorderlist()

            elif key == 'inventory':# 库存货信息

                Data(value).inventory()

            elif key == 'person':  # 个人信息

                Data(value).person()

            elif key == 'eb_tradelist':

                Data(value).eb_tradelist()

            elif key == 'saleoutlistall':

                Data(value).saleoutlistall()

            self.data_queue.task_done()

# 定时执行获取token
def runTask(day=0, hour=0, min=0, second=0):
    # Init time
    now = datetime.datetime.now()#返回一个当前的时间
    strnow = now.strftime('%Y-%m-%d %H:%M:%S')

    # First next run time
    period = datetime.timedelta(days=day, hours=hour, minutes=min, seconds=second)
    next_time = now + period
    strnext_time = next_time.strftime('%Y-%m-%d %H:%M:%S')

    while True:

        iter_now = datetime.datetime.now()
        iter_now_time = iter_now.strftime('%Y-%m-%d %H:%M:%S')
        if str(iter_now_time) == str(strnext_time):
            new_token = Token().run()
            global token
            token = new_token
            iter_time = iter_now + period
            strnext_time = iter_time.strftime('%Y-%m-%d %H:%M:%S')
            continue

        time.sleep(10)
        if data_queue.empty():
            break

#执行程序
def main():


    for i in range(2):
        try:
            loger().info('开启多线程执行请求任务')
            t = ThreadYongYout(url_queue)
            t.setDaemon(True)
            t.start()

        except Exception as error:
            loger().error('开启请求线程异常',error)


    for i in range(1):
        try:
            loger().info('开启线程获取queue数据')
            t = ThreadData(data_queue)
            t.setDaemon(True)
            t.start()
        except Exception as error:
            loger().error('开启线程请求queue异常',error)


    tok = threading.Thread(runTask(day=0, hour=1, min=30))
    tok.start()
    tok.join()

    time.sleep(4)

    url_queue.join()
    data_queue.join()

    if data_queue.empty():
        # print(data_queue.empty())
        tok.join()


if __name__ == '__main__':

    page_index = '1'
    end_url = 'from_account=bolebaokaifa&to_account=bolebao&app_key=opa87ad77a2a44f12df&token=' + \
              token + '&page_index=' + page_index + '&rows_per_page=20&ds_sequence=1'

    start_date = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    end_date = (datetime.date.today()).strftime("%Y-%m-%d ")

    # 销售订单信息
    order_url = 'https://api.yonyouup.com/api/saleorderlist/batch_get?' + end_url
    # 业务员信息
    person = 'https://api.yonyouup.com/api/person/batch_get?' + end_url
    # 客户信息
    customer = 'https://api.yonyouup.com/api/customer/batch_get?' + end_url
    # 产品档案
    inventory = 'https://api.yonyouup.com/api/inventory/batch_get?' + end_url
    # 出库单
    saleoutlistall = "https://api.yonyouup.com/api/saleoutlistall/batch_get?" + end_url
    # 电商订单
    eb_tradelist = 'https://api.yonyouup.com/api/eb_tradelist/batch_get?' + end_url

    list = [person]

    for i in list:
        url_queue.put(i)
        main()
