# encoding=utf-8
'''
此脚本是为了按照商品编码更改crm中u8对应的数据
'''
import json
import os
import queue
import re
import threading
import logging
import time
import curlify
import xml.etree.ElementTree as et
from suds.client import Client
import datetime
import http.client
from urllib import request,parse
from phone import Phone
#创建两个队列

url_queue = queue.Queue()
data_queue = queue.Queue()

#创建日志文件

root_path = os.getcwd()
log_path = root_path + '/Logs'
exist_file = os.path.exists(log_path)
if not exist_file:
    os.makedirs(log_path)

logger = logging.getLogger()
logger.setLevel(logging.INFO)
rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
log_path = os.path.dirname(os.getcwd()) + '/bolebaoproject/Logs/'


log_name = log_path + rq + '.log'
logfile = log_name
fh = logging.FileHandler(logfile, mode='w', encoding='utf-8')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
fh.setFormatter(formatter)
logger.addHandler(fh)

#webservice数据处理
def get_data():
    try:
        # 前一天时间
        # end_date = datetime.date.today() - datetime.timedelta(days=1)
        # strwhere="where dckdate = '%s'"%end_date
        url = 'http://124.207.40.126:9000/YouBlbWebGw/BLBServiceGW.asmx?WSDL'
        client = Client(url)
        # print(client)
        strwhere = "where dckdate >='2018-10-01' and dckdate<='2018-10-30'"

        res = client.service.GetU8OrderData(strwhere)
        return res
    except Exception as Error:
        logger.error(Error, )

def analytic_data():
    res=get_data()
    url='/api/v1.0/one/SN/'
    root = et.fromstring(res)
    for i in root:
        root_dict = {}
        for r in i:
            pass
        payload = {'objects': [root_dict]}
        post_meiqia(payload, url)


# 获取u8token信息
class Toekn():

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
            print('token为：', result['token']['id'])
            return result['token']['id']
        else:
            errcode = result['errcode']
            errmsg = result['errmsg']
            logger.error('获取token异常,异常码为%s，异常信息为%s' % (errcode, errmsg))
            # print('获取token异常，请重新请求')

token = Toekn().run()

# 线程类， 执行请求u8接口

#重写线程类
class ThreadYongYou(threading.Thread):

    def __init__(self, url_queue):
        threading.Thread.__init__(self)
        self.url_queue = url_queue

    # async def request(self, url):
    def request(self, url):
        dict = {}
        object = re.findall('\w+', url)[5]

        content_type = 'text/html'
        charset = 'utf-8'
        # 发起请求，并返回数据
        request_obj = request.Request(url)
        request_obj.add_header('Content-Type', content_type)
        request_obj.add_header('charset', charset)

        json_data = request.urlopen(request_obj).read().decode()
        # print(json_data)
        result = json.loads(json_data)
        dict[object] = result
        # print(self.name)
        return dict

    def run(self):
        logger.info('开始发送url请求')
        while True:
            # if url_queue.empty() == True:
            #     # print(url_queue.empty())
            #     self.url_queue.task_done()
            #     break
            url = self.url_queue.get()
            old_token = url.split('&')[3].split('=')[1]
            old_token = 'token=' + old_token
            new_token = 'token=' + token
            url = re.sub(old_token, new_token, url)

            try:
                result = ThreadYongYou.request(self, url)
                # result = loop.run_until_complete(ThreadYongYou.request(self, url))

                # 判断返回结果是否为空
                if len(result) == None:
                    logger.error('第1次请求%s异常，异常信息为：%s' % (url, result))
                    i = 1
                    while i < 3:
                        # result = loop.run_until_complete(ThreadYongYou.request(self, url))

                        result = ThreadYongYou.request(self, url)
                        if len(result) == None:
                            logger.error('第%s次请求%s异常，异常信息为：%s' %
                                         (i + 1, url, result))

                        else:
                            # (key, value), = result.items()
                            # if value['errcode'] != "0":
                            #     break
                            data_queue.put(result)
                            break
                        i += 1


                else:
                    # 添加数据到dat_queue

                    (key, value), = result.items()
                    if value['errcode'] == '0':
                        data_queue.put(result)


            except Exception as error:
                logger.error(error, url,)
            self.url_queue.task_done()


#执行查询插入操作
def post_meiqia(url,payload=None):
    textmod=payload
    header_dict = {
        'x-token': "AexZAHT6jVsAAEFRQUNRcXdlQWhjQkFBQUFWdFlLWGRDeFJoVlZiQUFBQVFBQ1Fxd2VYUkVCQUFBQTM1eDc2WkhsTEJVWXBRQUH-wsHHEfENv8rexZmz2t9NygV2o2Ar5FP75JgrwV8vqFwSE1mZPne4ru8o0euVwWcRg87HsXqzguyvJNiPWu2o",
        'content-type': "application/json",
        'cache-control': "no-cache",
        'postman-token': "529a9a27-2e62-0d64-aea9-c938d33ec5fd"
        }
    url = "https://crm.meiqia.com" + url
    # print(url)
    # print(textmod)
    if textmod:
        try:
            # json串数据使用
            textmod = json.dumps(textmod).encode(encoding='utf-8')
            req = request.Request(url=url, data=textmod, headers=header_dict)
            res = request.urlopen(req)
            res = res.read().decode(encoding='utf-8')
            res_data = json.loads(res)
            logging.warning(res_data)
            print(res_data)

            # if res_data['code'] != 0:
            #     res_payload = payload
            #     res_url = url
            #     post_meiqia(res_payload, res_url)

        except Exception as Error:
            # print("出错了")
            logger.error(Error)
    else:
        try:
            req = request.Request(url = url,headers = header_dict)
            res = request.urlopen(req)
            # print(res)
            res = res.read().decode(encoding = 'utf-8')
            return json.loads(res)['body']['objects']
        except Exception as Error:
            logger.error(Error)
#更改数据
def put_meiqia(payload, url):
    try:
        conn = http.client.HTTPSConnection("crm.meiqia.com")#连接指定的服务器
        payload = json.dumps(payload)
        headers = {
            'x-token': "AexZAHT6jVsAAEFRQUNRcXdlQWhjQkFBQUFWdFlLWGRDeFJoVlZiQUFBQVFBQ1Fxd2VYUkVCQUFBQTM1eDc2WkhsTEJVWXBRQUH-wsHHEfENv8rexZmz2t9NygV2o2Ar5FP75JgrwV8vqFwSE1mZPne4ru8o0euVwWcRg87HsXqzguyvJNiPWu2o",
            'content-type': "application/json",
            'cache-control': "no-cache",
            'postman-token': "529a9a27-2e62-0d64-aea9-c938d33ec5fd"
        }

        conn.request("PUT", url, payload, headers)#使用指定的方法和url向服务器发送请求

        res = conn.getresponse()#返回一个 HTTPResponse 实例
        data = res.read().decode("utf-8")#读取内容

        data=json.loads(data)
        logging.warning(data)
        print(data)

        conn.close()
    except Exception as Error:
        logger.error(Error)
#处理电话号码
def phone(dict_c,phe):

    if phe.startswith('0'):
        if len(phe) == 11:
            dict_c['ChannelPhone'] = "+86 " + phe
        elif len(phe) == 12 and "-" in phe:
            dic = phe.split("-")
            dict_c['ChannelPhone'] = "+86 " + dic[0] + dic[1]
        elif len(phe) > 12:
            dict_c['Remarks'] = phe
    else:
        dict_c['Remarks']=phe
    return dict_c

#处理手机号
def mobile(dict_c,mbe):

    if len(mbe) == 11:
        dict_c['ChannelPhone'] = '+86 ' + mbe
    elif len(mbe) > 11:
        aa = '(13\d|14[5|7]|15\d|166|17[3|6|7]|18\d)\d{8}'
        dit = re.search(aa, mbe).group()
        dict_c['ChannelPhone'] = '+86 ' + dit
        dict_c['Remarks'] = mbe
    return dict_c

#执行查询更改操作
def data_query(data):
    red = data
    data_url = '/api/v1.0/one/dsl/query?dsl={"Product":{"fields":"id","cond":{"==":{"ProductNumber":"' + red['ProductNumber'] + '"}}}}'
    red_id = post_meiqia(data_url)
    print(red_id)
    if red_id:
        red_url = '/api/v1.0/one/Product/'+red_id[0]['id']
        reds = red.pop('ProductNumber')
        red["version"]=red_id[0]['version']
        put_meiqia(red,red_url)
def saleout_query(data):
    red = data
    data_url = '/api/v1.0/one/dsl/query?dsl={"OrderInfo":{"fields":["id","LogisticsNumber"],"cond":{"==":{"name":"' + red['code'] + '"}}}}'
    red_id = post_meiqia(data_url)

    print(red_id)
    if red_id:
        if red_id[0]['LogisticsNumber']:
            red['LogisticsNumber'] = red['LogisticsNumber']+ ";"+red_id[0]['LogisticsNumber']
        red_url = '/api/v1.0/one/Product/'+red_id[0]['id']
        reds = red.pop('code')
        red['version']=red_id[0]['version']
        put_meiqia(red,red_url)

def revise_data(re_data):

    revise_data = re_data
    revise_url = '/api/v1.0/one/dsl/query?dsl={"Tickets_ReturnGoods":{"fields":"id","cond":{"==":{"XSNumbers":"' + revise_data['code'] + '"}}}}'
    revise_id = post_meiqia(revise_url)
    if revise_id:
        rev_url = '/api/v1.0/one/Tickets_ReturnGoods/'+revise_id[0]['id']
        revise_data['version'] = revise_id[0]['version']
        put_meiqia(revise_data,rev_url)

#查询并返回省，市，区的id
def get_id(object_name,record):

    get_url = '/api/v1.0/one/dsl/query?dsl={"'+object_name+'":{"fields":"id","cond":{"==":{"name":"' + parse.quote(record) + '"}}}}'
    obj_id = post_meiqia(get_url)
    # print(obj_id)
    return obj_id

#  处理data_queue的数据
class ThreadData(threading.Thread):

    def __init__(self, data_queue):
        threading.Thread.__init__(self)
        self.data_queue = data_queue
        self.data = []

    def run(self):

        while True:
            # if self.data_queue.empty() == True:
            #     time.sleep(5)
            #     if self.data_queue.empty() == True:
            #         break

            data = self.data_queue.get()
            (key, value), = data.items()

            print(value)

            if key == 'inventory':# 库存货信息
                url = "/api/v1.0/one/Product/"
                data = value['inventory']
                print(data)
                list_i = []


                dict_i = {}
                dict_i['ProductNumber'] = data['code']
                dict_i['TaxUnitPrice'] = float(data['fRetailPrice'])
                data_query(dict_i)

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
            new_token = Toekn().run()
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

    for i in range(1):
        try:
            logger.info('开启多线程执行请求任务')
            t = ThreadYongYou(url_queue)
            t.setDaemon(True)
            t.start()

        except Exception as error:
            logger.error('开启请求线程异常')
            print(error)

    for i in range(1):
        try:
            logger.info('开启线程获取queue数据')
            t = ThreadData(data_queue)
            t.setDaemon(True)
            t.start()
        except Exception as error:
            logger.error('开启线程请求queue异常')
            print(error)

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
    # token = Toekn.run()
    aa = ['AE03000019','AE03000020']
    end_url = 'from_account=bolebaokaifa&to_account=bolebao&app_key=opa87ad77a2a44f12df&' \
              'token=628b1c30186845ff9ef57602390ea1dc&id='
    #产品档案
    inventory = 'https://api.yonyouup.com/api/inventory/get?' + end_url

    for i in aa:
        url_queue.put(inventory+i)
        main()
