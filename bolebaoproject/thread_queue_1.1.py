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
import asyncio

url_queue = queue.Queue()
data_queue = queue.Queue()

root_path = os.getcwd()
log_path = root_path + '/Logs'
exist_file = os.path.exists(log_path)
if not exist_file:
    os.makedirs(log_path)

logger = logging.getLogger()
logger.setLevel(logging.INFO)
rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
log_path = os.path.dirname(log_path)
print(log_path)
# os.makedirs(log_path)
log_name = log_path + rq + '.log'
logfile = log_name
fh = logging.FileHandler(logfile, mode='w', encoding='utf-8')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    "%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
fh.setFormatter(formatter)
logger.addHandler(fh)
loop = asyncio.get_event_loop()


# 获取u8token信息
class Toekn(object):

    def __init__(self):
        self.content_type = 'text/html'
        self.charset = 'utf-8'

    def run(self):
        url = 'https://api.yonyouup.com/system/token?from_account=bolebaokaifa&app_key=opa87ad77a2a44f12df&app_secret=7027dd0c880141308bedc8bfd0b854c9'
        request = Request(url)
        request.add_header('Content-Type', self.content_type)
        request.add_header('charset', self.charset)

        json_data = urlopen(request).read().decode()
        result = json.loads(json_data)
        if len(result) > 0:
            print('token为：', result['token']['id'])
            return result['token']['id']
        else:
            errcode = result['errcode']
            errmsg = result['errmsg']
            logger.error('获取token异常,异常码为%s，异常信息为%s' % (errcode, errmsg))
            print('获取token异常，请重新请求')

token = Toekn().run()

# 线程类， 执行请求u8接口


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
        print(self.name)
        return dict

    def run(self):
        logger.info('开始发送url请求')
        while True:
            url = self.url_queue.get()
            old_token = url.split('&')[3].split('=')[1]
            old_token = 'token=' + old_token
            new_token = 'token=' + token
            url = re.sub(old_token, new_token, url)

            print(url, 1111)
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
                    page_count = value['page_count']
                    print(page_count, 22222)
                    pagenum = re.findall(
                        r'page_index=\d+', url)[0].split('=')[1]

                    if int(pagenum) == 1:
                        page = 2
                        while int(page) <= int(page_count):
                            pages = 'page_index=' + str(page)
                            url_list = url.split('page_index=1')

                            next_url = url_list[0] + pages + url_list[1]
                            print(next_url)
                            url_queue.put(next_url)
                            page += 1
            except Exception as error:
                logger.error(error, url, )
            self.url_queue.task_done()


#  执行插入操作
def post_meiqia(payload, url):
    try:
        conn = http.client.HTTPSConnection("crm.meiqia.com")

        # payload = {"objects": [{"name": "+86 18811111111", "UserName": "王二"}]}
        payload = json.dumps(payload)
        headers = {
            'x-token': "AexZAHT6jVsAAEFRQUNRcXdlQWhjQkFBQUFWdFlLWGRDeFJoVlZiQUFBQVFBQ1Fxd2VYUkVCQUFBQTM1eDc2WkhsTEJVWXBRQUH-wsHHEfENv8rexZmz2t9NygV2o2Ar5FP75JgrwV8vqFwSE1mZPne4ru8o0euVwWcRg87HsXqzguyvJNiPWu2o",
            'content-type': "application/json",
            'cache-control': "no-cache",
            'postman-token': "529a9a27-2e62-0d64-aea9-c938d33ec5fd"
        }

        conn.request("POST", url, payload, headers)

        res = conn.getresponse()
        data = res.read()

        print(data.decode("utf-8"))
    except Exception as Error:
        logger.error(Error, )


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
            print(type(data), key, value)

            if key == 'customer':
                url = "/api/v1.0/one/UserArchives/"
                data = value['customer']
                for i in data:
                    code = i['code']
                    name = i['name']
                    abbrname = i['abbrname']
                    sort_code = i['sort_code']
                    if 'bank_open' in i:
                        bank_open = ['bank_open']
                    if 'bank_acc_number' in i:
                        bank_acc_number = i['bank_acc_number']
                    if 'address' in i:
                        address = i['address']
                    if 'contact' in i:
                        contact = i['contact']
                    if 'mobile' in i:
                        mobile = i['mobile']
                    if 'devliver_site' in i:
                        devliver_site = i['devliver_site']
                    if 'spec_operator' in i:
                        spec_operator = i['spec_operator']
                    if 'spec_operator_name' in i:
                        spec_operator_name = i['spec_operator_name']
                    ccusexch_name = i['ccusexch_name']
                    bcusdomestic = i['bcusdomestic']
                    bcusoverseas = i['bcusoverseas']
                    bserviceattribute = i['bserviceattribute']
                    ccusmngtypecode = i['ccusmngtypecode']
                    ccusmngtypename = i['ccusmngtypename']
                    payload = {"objects": [
                        {"name": "+86 18811111111", "UserName": "王二"}]}
                    loop.run_until_complete(post_meiqia(payload, url))

            elif key == 'saleorderlist':
                url = "/api/v1.0/one/OrderInfo/"
                data = value['saleorderlist']
                list_s=[]
                for i in data:
                    dict_s={}
                    dict_s['Code'] = i['code']  # 订单号
                    dict_s['OrderTime'] = i['date']  # 日期
                    dict_s['BusinessType'] = i['businesstype']  # 业务类型
                    dict_s['TypeCode'] = i['typecode']  # 销售类型编码
                    dict_s['TypeName'] = i['typename']  # 销售类型
                    dict_s['State'] = i['state']  # 单据状态
                    dict_s['Custcode'] = i['custcode']  # 客户编码
                    dict_s['Cusname'] = i['cusname']  # 客户名称
                    dict_s['Cusabbname'] = i['cusabbname']  # 客户简称
                    dict_s['Deptcode'] = i['deptcode']  # 部门编码
                    dict_s['Deptname'] = i['deptname']  # 部门名称
                    dict_s['Personcode'] = i['personcode']  # 人员编码
                    dict_s['PersonName'] = i['personname']  # 人员
                    dict_s['Sendaddress'] = i['sendaddress']  # 发货地址
                    dict_s['Dpremodatebt'] = i['dpremodatebt']  # 预完工日期
                    dict_s['Dpredatebt'] = i['dpredatebt']  # 预发货日期
                    dict_s['Maker'] = i['maker']  # 制单人
                    dict_s['Verifier'] = i['verifier']  # 审核人
                    if 'define14' in i:
                        dict_s['Define14'] = i['define14']  # 地址
                    dict_s['Money'] = i['money']  # 无税金额
                    dict_s['Sum'] = i['sum']  # 价税合计
                    if 'fhstatus' in i:
                        dict_s['Fhstatus'] = i['fhstatus']  # 发货状态(0=未发货;1=部分发货;2=全部发货)
                    list_s.append(dict_s)
                payload={"objects":list_s}
                loop.run_until_complete(post_meiqia(payload, url))

            elif key == 'inventory':
                url = "/api/v1.0/one/Product/"
                data = value['inventory']
                list_i = []
                for i in data:
                    dict_i={}
                    dict_i['ProductNumber'] = i['code']  # 存货编码
                    dict_i['name'] = i['name']  # 存货名称
                    if "specs" in i:
                        dict_i['Specs'] = i['specs']  # 规格型号
                    dict_i['"ProductSortCode'] = i['sort_code']  # 所属分类码
                    dict_i['ProductSortName'] = i['sort_name']  # 所属分类名称
                    dict_i['MainMeasure'] = i['main_measure']  # 主计量单位
                    dict_i['Unit'] = i['ccomunitname']  # 单位
                    dict_i['StartDate'] = i['start_date']  # 启用时间
                    dict_i['ModifyDate'] = i['modifydate']  # 变更时间
                    dict_i['ProductIsupplyType'] = i['isupplytype']  # 供应类型
                    dict_i['Imptaxrate'] = i['iimptaxrate']  # 进项税率
                    dict_i['TaxRate'] = i['tax_rate']  # 销售税率
                    if i['sale_flag']=="1":
                        dict_i['SaleFlay'] = "是"  # 是否内销
                    else:
                        dict_i["SaleFlay"]="否"

                    if i['bexpsale']=="1":# 是否外销
                        dict_i['Bexpsale'] ="是"
                    else:
                        dict_i['Bexpsale'] = "否"
                    dict_i['Entry'] = i['entry']  # 存货编码
                    list_i.append(dict_i)
                payload = {"objects": list_i}
                loop.run_until_complete(post_meiqia(payload, url))

            self.data_queue.task_done()


# 定时执行获取token
def runTask(day=0, hour=0, min=0, second=0):
    # Init time
    now = datetime.now()#返回一个当前的时间
    strnow = now.strftime('%Y-%m-%d %H:%M:%S')
    print("now:", strnow)

    # First next run time
    period = timedelta(days=day, hours=hour, minutes=min, seconds=second)
    next_time = now + period
    strnext_time = next_time.strftime('%Y-%m-%d %H:%M:%S')
    print("next run:", strnext_time)

    while True:
        # Get system current time
        iter_now = datetime.now()
        iter_now_time = iter_now.strftime('%Y-%m-%d %H:%M:%S')
        if str(iter_now_time) == str(strnext_time):
            # Get every start work time
            print("start work: %s" % iter_now_time)

            # Call task func

            new_token = Toekn().run()
            global token
            token = new_token

            # Get next iteration time
            iter_time = iter_now + period
            strnext_time = iter_time.strftime('%Y-%m-%d %H:%M:%S')
            print("next_iter: %s" % strnext_time)

            # Continue next iteration
            continue

        time.sleep(20)
        if data_queue.empty():
            print(data_queue.empty(), 11111)

            break


def main():

    # 批量获取客户信息
    page_index = '1'

    end_url = 'from_account=bolebaokaifa&to_account=bolebao&app_key=opa87ad77a2a44f12df&token=' + \
        token + '&page_index=' + page_index + '&rows_per_page=20&ds_sequence=1'

    # 销售订单信息
    order_url = 'https://api.yonyouup.com/api/saleorderlist/batch_get?' + end_url
    # 客户信息
    customer = 'https://api.yonyouup.com/api/customer/batch_get?' + end_url
    # 客户分类
    customerclass = 'https://api.yonyouup.com/api/customerclass/batch_get?'

    # 库存分类
    # inventoryclass = 'https://api.yonyouup.com/api/inventoryclass/batch_get?' +end_url
    # 库存货信息
    inventory = 'https://api.yonyouup.com/api/inventory/batch_get?' + end_url
    # list = [customer, order_url, inventory]
    list = [customer]

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
            print(error)

    for i in range(4):
        try:
            logger.info('开启线程获取queue数据')
            t = ThreadData(data_queue)
            t.setDaemon(True)
            t.start()
        except Exception as error:
            logger.error('开启线程请求queue异常')
            print(error)
    time.sleep(4)

    tok = threading.Thread(runTask(day=0, hour=1, min=50))
    tok.start()
    tok.join()

    url_queue.join()
    data_queue.join()
    if data_queue.empty():
        print(data_queue.empty())
        tok.join()


if __name__ == '__main__':
    main()
