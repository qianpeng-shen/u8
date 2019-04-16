# encoding=utf-8
import json
import os
import queue
import re
import threading
import logging
import time
from datetime import datetime, timedelta
from urllib.request import Request, urlopen
import http.client
import datetime

#创建两个队列
tad_queue = queue.Queue()
url_queue = queue.Queue()
data_queue = queue.Queue()

#创建日志文件

root_path = os.getcwd()  # 返回当前工作目录
log_path = root_path + '/Logs'
exist_file = os.path.exists(log_path)  # 判断路径是否存在，返回True和False

if not exist_file:  # 如果不存在,递归创建目录
    os.makedirs(log_path)


logger = logging.getLogger()  # 获取logger对象
logger.setLevel(logging.INFO)  # 设置logger的级别为logging.info
rq = time.strftime('%Y%m%d%H%M', time.localtime(
    time.time()))  # 返回以%Y%m%d%H%M为格式的时间字符串
log_path = os.path.dirname(log_path)  # 获取文件的所在目录
# print(log_path)

# os.makedirs(log_path)
log_name = log_path + rq + '.log'
logfile = log_name
# 把日志记录记录在logfile文件中，模式为"w",编码为utf8
fh = logging.FileHandler(logfile, mode='w', encoding='utf-8')
fh.setLevel(logging.DEBUG)  # 设置文件的级别为debug
# 设置日志格式
formatter = logging.Formatter(
    "%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
#%(asctime)s 字符串形式的当前时间,%(filename)s 调用日志输出函数的模块的文件名,%(lineno)d 调用日志输出函数的语句所在的代码行,
#%(levelname)s 文本形式的日志级别,%(message)s 用户输出的消息
fh.setFormatter(formatter)
# 将相应的handler添加在logger对象中
logger.addHandler(fh)



# 获取u8token信息
class Toekn(object):

    def __init__(self):
        self.content_type = 'text/html'
        self.charset = 'utf-8'

    def run(self):
        url = 'https://api.yonyouup.com/system/token?from_account=bolebaokaifa&app_key=opa87ad77a2a44f12df&app_secret=7027dd0c880141308bedc8bfd0b854c9'
        request = Request(url)#创建一个Request对象
        #使用add_header方法向request中添加请求头,也可以在Requst中直接添加请求头
        request.add_header('Content-Type', self.content_type)
        request.add_header('charset', self.charset)
        #发送请求并转换
        json_data = urlopen(request).read().decode()
        result = json.loads(json_data)#转换为字典
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

    def __init__(self, url_queue, token):
        threading.Thread.__init__(self)
        self.url_queue = url_queue

    # async def request(self, url):
    def request(self, url):
        dict = {}
        object = re.findall('\w+', url)[5]

        content_type = 'text/html'
        charset = 'utf-8'
        # 发起请求，并返回数据
        request = Request(url)
        request.add_header('Content-Type', content_type)
        request.add_header('charset', charset)

        json_data = urlopen(request).read().decode()
        result = json.loads(json_data)
        dict[object] = result
        # print(self.name)
        return dict

    def run(self):
        logger.info('开始发送url请求')
        while True:
            url = self.url_queue.get()

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
                            data_queue.put(result)
                            break
                        i += 1

                else:
                    # 添加数据到dat_queue
                    data_queue.put(result)
                    (key, value), = result.items()
                    # print(value)
                    page_count = value['page_count']
                    # print(page_count, 22222)
                    pagenum = re.findall(
                        r'page_index=\d+', url)[0].split('=')[1]

                    if int(pagenum) == 1:
                        page = 2
                        while int(page) <= int(page_count):
                            pages = 'page_index=' + str(page)
                            url_list = url.split('page_index=1')

                            next_url = url_list[0] + pages + url_list[1]
                            # print(next_url)
                            url_queue.put(next_url)
                            page += 1
            except Exception as error:
                logger.error(error, url, )
            self.url_queue.task_done()


#执行插入操作
def post_meiqia(payload, url):
    try:
        conn = http.client.HTTPSConnection("crm.meiqia.com")#连接指定的服务器
        payload = json.dumps(payload)
        headers = {
            'x-token': "AexZAHT6jVsAAEFRQUNRcXdlQWhjQkFBQUFWdFlLWGRDeFJoVlZiQUFBQVFBQ1Fxd2VYUkVCQUFBQTM1eDc2WkhsTEJVWXBRQUH-wsHHEfENv8rexZmz2t9NygV2o2Ar5FP75JgrwV8vqFwSE1mZPne4ru8o0euVwWcRg87HsXqzguyvJNiPWu2o",
            'content-type': "application/json",
            'cache-control': "no-cache",
            'postman-token': "529a9a27-2e62-0d64-aea9-c938d33ec5fd"
        }

        conn.request("POST", url, payload, headers)#使用指定的方法和url向服务器发送请求

        res = conn.getresponse()#返回一个 HTTPResponse 实例
        data = res.read().decode("utf-8")#读取内容

        data=json.loads(data)
        print(data)
        # if data['code'] != 0:
        #     dict_data={}
        #     dict_data['url']=url
        #     dict_data['payload']=payload
        #     tad_queue.put(dict_data)

        conn.close()
    except Exception as Error:
        logger.error(Error, )

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
def mobile(dict_c,mbe):
    if len(mbe) == 11:
        dict_c['ChannelPhone'] = '+86 ' + mbe
    elif len(mbe) > 11:
        aa = '(13\d|14[5|7]|15\d|166|17[3|6|7]|18\d)\d{8}'
        dit = re.search(aa, mbe).group()
        dict_c['ChannelPhone'] = '+86 ' + dit
        dict_c['Remarks'] = mbe
    return dict_c
#  处理data_queue的数据
class ThreadData(threading.Thread):

    def __init__(self, data_queue):
        threading.Thread.__init__(self)
        self.data_queue = data_queue
        self.data = []

    def run(self):
        while True:
            data = self.data_queue.get()
            (key, value), = data.items()
            # print(type(data), key, value)

            if key == 'customer':
                url = "/api/v1.0/one/Channel/"
                data = value['customer']
                list_c=[]
                for i in data:
                    dict_c={}
                    dict_c['name'] = i['name']  # 购买渠道
                    if 'address' in i:
                        dict_c['ChannelAddress']=i['address']
                    if 'contact' in i:
                        dict_c['ChannelContact'] = i['contact']  # 联系人
                    #考虑手机号和电话的情况
                    if 'mobile' in i or 'phone' in i:
                        if 'mobile' in i and 'phone' in i:
                            if i['mobile'] and i['phone']:
                                if i['mobile'] == i['phone']:
                                    if len(i['mobile']) == 11:
                                        dict_c['ChannelPhone']="+86 "+i['mobile']
                                    elif len(i['mobile']) == 12 and "-" in i['mobile']:
                                        dic = i['phone'].split("-")
                                        dict_c['ChannelPhone'] = "+86 " + dic[0] + dic[1]
                                    elif len(i['mobile'])>11 and "-" not in i['mobile']:
                                        dict_c['Remarks']=i['mobile']

                                elif  i['mobile'] != i['phone']:
                                    if len(i['mobile'])==11:
                                        dict_c['ChannelPhone'] = "+86 " + i['mobile']
                                        dict_c['Remarks']=i['phone']
                                    elif len(i['mobile']) > 11:
                                        aa='(13\d|14[5|7]|15\d|166|17[3|6|7]|18\d)\d{8}'
                                        dit =re.search(aa, i['mobile']).group()
                                        dict_c['name']='+86 '+ dit
                                        dict_c['Remarks']=i['mobile']+i['phone']

                            elif i['phone'] and not i['mobile'] :
                                phone(dict_c,i['phone'])
                            elif i['mobile'] and not i['phone']:
                                mobile(dict_c, i['mobile'])

                        elif 'mobile' in i and 'phone' not in i:
                            if i['mobile']:
                                mobile(dict_c,i['mobile'])
                        elif 'mobile' not in i and 'phone' in i:
                            if i['phone']:
                                phone(dict_c, i['phone'])
                    list_c.append(dict_c)

                payload = {"objects": list_c}

                post_meiqia(payload, url)
            elif key == 'inventory':# 库存货信息
                url = "/api/v1.0/one/Product/"
                data = value['inventory']
                # print(data)
                list_i = []
                for i in data:
                    dict_i = {}
                    if 'end_date' in i:
                        if i['end_date']:
                            continue
                    dict_i['ProductNumber'] = i['code']  # 产品编码
                    dict_i['name'] = i['name']  # 存货名称
                    if "specs" in i:
                        dict_i['Specs'] = i['specs']  # 规格型号
                    dict_i['ProductSortCode'] = i['sort_code']  # 所属分类码
                    dict_i['ProductSortName'] = i['sort_name']  # 所属分类名称
                    dict_i['MainMeasure'] = i['main_measure']  # 主计量单位
                    dict_i['Unit'] = i['ccomunitname']  # 单位
                    dict_i['StartDate'] = i['start_date'].split(" ")[0] + "T" + \
                                          i['start_date'].split(" ")[1].split(".")[0] + "Z"  # 启用时间
                    if 'modifydate' in i:
                        dict_i['ModifyDate'] = i['modifydate'].split(" ")[0] + "T" + \
                                           i['modifydate'].split(" ")[1].split(".")[0] + "Z"  # 变更时间
                    if 'isupplytype' in i:
                        dict_i['ProductIsupplyType'] = i['isupplytype']  # 供应类型
                    dict_i['Imptaxrate'] = float(i['iimptaxrate'])/100  # 进项税率
                    dict_i['TaxRate'] = float(i['tax_rate'])/100  # 销售税率
                    if 'ref_sale_price' in i:
                        dict_i['Price']=float(i['ref_sale_price'])#单价
                    if 'bbarcode' in i:
                        dict_i['Bbarcode']=i['bbarcode']#条形码管理
                    if 'defwarehousename' in i:
                        dict_i['Defwarehousename']=i['defwarehousename']#默认仓库名称
                    if 'defwarehouse' in i:
                        dict_i['Defwarehouse']=i['defwarehouse']#默认仓库
                    if 'self_define1' in i:
                        dict_i['SelfDefine1']=i['self_define1']
                    if 'sale_flag' in i:
                        if i['sale_flag'] == "1":
                            dict_i['SaleFlag'] = "是"  # 是否内销
                        else:
                            dict_i["SaleFlag"] = "否"
                    if 'bexpsale' in i:
                        if i['bexpsale'] == "1":  # 是否外销
                            dict_i['Bexpsale'] = "是"
                        else:
                            dict_i['Bexpsale'] = "否"
                    if 'entry' in i:
                        if 'invcode' in i['entry'][0]:
                            dict_i['Entry'] = i['entry'][0]['invcode']  # 存货编码
                        if 'partid' in i['entry'][0]:
                            dict_i['Partid']=i['entry'][0]['partid']

                    list_i.append(dict_i)
                # payload = {"objects": list_i}
                # post_meiqia(payload, url)
            elif key == 'person':  # 个人信息
                url = "/api/v1.0/one/Salesman/"
                data = value['person']
                # print(data)
                list_p = []
                for i in data:
                    dict_p={}
                    dict_p["name"]=i["name"]
                    dict_p["PersonnelNumber"]=i["code"]
                    dict_p["DepartmentName"]=i["cdept_name"]
                    dict_p["DepartmentCode"]=i["cdept_num"]
                    list_p.append(dict_p)
                    payload = {"objects": list_p}
                    # print(payload)
                    post_meiqia(payload, url)
                    time.sleep(0.5)
            self.data_queue.task_done()
def main():
    page_index = '1'
    end_url = 'from_account=bolebaokaifa&to_account=bolebao&app_key=opa87ad77a2a44f12df&token=' + \
        token + '&page_index=' + page_index + '&rows_per_page=20&ds_sequence=1'
    # 销售订单信息
    order_url = 'https://api.yonyouup.com/api/saleorderlist/batch_get?' + end_url
    # 客户信息
    customer = 'https://api.yonyouup.com/api/customer/batch_get?' + end_url
    # 库存货信息
    inventory = 'https://api.yonyouup.com/api/inventory/batch_get?' + end_url
    #业务员信息
    person = 'https://api.yonyouup.com/api/person/batch_get?' + end_url



    list = [inventory]

    for i in list:
        url_queue.put(i)

    for i in range(2):
        try:
            logger.info('开启多线程执行请求任务')
            t = ThreadYongYou(url_queue, token)
            t.setDaemon(True)
            t.start()
        except Exception as error:
            logger.error('开启请求线程异常')
            # print(error)

    for i in range(3):
        try:
            logger.info('开启线程获取queue数据')
            t = ThreadData(data_queue)
            t.setDaemon(True)
            t.start()
        except Exception as error:
            logger.error('开启线程请求queue异常')
            # print(error)

    if not tad_queue.empty():
        data=tad_queue.get()
        if data:
            print(data)
            post_meiqia(data['payload'],data['url'])
            tad_queue.task_done()

    time.sleep(4)

    tad_queue.join()
    url_queue.join()
    data_queue.join()



if __name__ == '__main__':
    main()
