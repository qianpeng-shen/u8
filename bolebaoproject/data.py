# encoding=utf-8
import http.client
import json
import re
import queue
import threading
import datetime
from urllib import request,parse

url_queue = queue.Queue()
data_queue = queue.Queue()

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

            print('获取token异常，请重新请求')



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

        while True:
            url = self.url_queue.get()
            try:
                result = ThreadYongYou.request(self, url)

                # 判断返回结果是否为空
                if len(result) == None:
                    print('第1次请求%s异常，异常信息为：%s' % (url, result))
                    i = 1
                    while i < 3:
                        # result = loop.run_until_complete(ThreadYongYou.request(self, url))

                        result = ThreadYongYou.request(self, url)
                        if len(result) == None:
                            print('第%s次请求%s异常，异常信息为：%s' %
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
                    if value['errcode'] != "0":
                        continue

                    data_queue.put(result)

                    pagenum_data = re.findall(
                        r'page_index=\d+', url)[0]
                    pagenum = pagenum_data.split('=')[1]

                    if int(pagenum) == 2230 :
                        page = int(pagenum) + 1
                        while int(page) <= 2269:
                            pages = 'page_index=' + str(page)
                            url_list = url.split('%s' %(pagenum_data))

                            next_url = url_list[0] + pages + url_list[1]
                            url_queue.put(next_url)
                            page += 1
            except Exception as error:
                print(error)
            self.url_queue.task_done()

def put_meiqia(url,data):

    conn = http.client.HTTPSConnection("crm.meiqia.com")#连接指定的服务器
    # payload = json.dumps(payload)
    headers = {
        'x-token': "AexZAHT6jVsAAEFRQUNRcXdlQWhjQkFBQUFWdFlLWGRDeFJoVlZiQUFBQVFBQ1Fxd2VYUkVCQUFBQTM1eDc2WkhsTEJVWXBRQUH-wsHHEfENv8rexZmz2t9NygV2o2Ar5FP75JgrwV8vqFwSE1mZPne4ru8o0euVwWcRg87HsXqzguyvJNiPWu2o",
        'content-type': "application/json",
        'cache-control': "no-cache",
        'postman-token': "529a9a27-2e62-0d64-aea9-c938d33ec5fd"
    }
    conn.request("DELETE",url,headers=headers)#使用指定的方法和url向服务器发送请求
    res = conn.getresponse()#返回一个 HTTPResponse 实例
    data = res.read().decode("utf-8")#读取内容

    data=json.loads(data)
    print(data)

    conn.close()
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
            print(res_data)

        except Exception as Error:
            print("1出错了")
    else:
        try:
            req = request.Request(url = url,headers = header_dict)
            res = request.urlopen(req)
            # print(res)
            res = res.read().decode(encoding = 'utf-8')
            return json.loads(res)['body']['objects']
        except Exception as Error:
            print("2")
def fun():
    aa = "OrderInfo"
    revise_url = '/api/v1.0/one/dsl/query?dsl={"'+aa+'":{"fileds":"id"}}'
    one_url = '/api/v1.0/one/OrderInfo/query?fields=["id","owner","wheel"]'
    aa = post_meiqia(revise_url)

    for i in aa:
        two_url = '/api/v1.0/one/OrderInfo/'+i['id']+'/?version='+str(i['version'])
        put_meiqia(two_url)
class ThreadData(threading.Thread):

    def __init__(self, data_queue):
        threading.Thread.__init__(self)
        self.data_queue = data_queue
        self.data = []

    def run(self):

        while True:

            data = self.data_queue.get()
            (key, value), = data.items()
            print(value)
            if key == 'saleorderlist':

                data = value['saleorderlist']
                for i in data:
                    data_url = '/api/v1.0/one/dsl/query?dsl={"OrderInfo":{"fileds":"id","cond":{"==":{"name":"' + i['code'] + '"}}}}'
                    order = post_meiqia(data_url)
                    print(order)
                    two_url = '/api/v1.0/one/OrderInfo/' + order['id'] + '/?version=' + str(order['version'])
                    # put_meiqia(two_url)
def main():
    token = Toekn().run()
    page_index = '2230'
    end_url = 'from_account=bolebaokaifa&to_account=bolebao&app_key=opa87ad77a2a44f12df&token=' + \
        token + '&page_index=' + page_index + '&rows_per_page=20&ds_sequence=1'

    order_url = 'https://api.yonyouup.com/api/saleorderlist/batch_get?' + end_url

    list = [order_url]

    for i in list:
        url_queue.put(i)

    for i in range(2):
        try:
            t = ThreadYongYou(url_queue)
            t.setDaemon(True)
            t.start()

        except Exception as error:
            print(error)

    for i in range(1):
        try:
            t = ThreadData(data_queue)
            t.setDaemon(True)
            t.start()
        except Exception as error:
            print(error)

if __name__ == '__main__':

    main()