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
        data = res.read()#读取内容
        print(data.decode("utf-8"))
        conn.close()
    except Exception as Error:
        logger.error(Error, )

def phone(dict_c,phe):
    if phe.startswith('1'):
        if len(phe) == 11:
            dict_c['name'] = "+86 " + phe
        elif len(phe) == 12 and "-" in phe:
            dic = phe.split("-")
            dict_c['name'] = "+86 " + dic[0] + dic[1]
        elif len(phe) > 12:
            dict_c['name'] = "+86 18175368569"
            dict_c['Remarks'] = phe
    else:
        dict_c['Remarks']=phe
    return dict_c
def mobile(dict_c,mbe):
    if len(mbe) == 11:
        dict_c['name'] = '+86 ' + mbe
    elif len(mbe) > 11:
        aa = '(13\d|14[5|7]|15\d|166|17[3|6|7]|18\d)\d{8}'
        dit = re.search(aa, mbe).group()
        dict_c['name'] = '+86 ' + dit
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
                    dict_c['Code'] = i['code']  # 用户编码
                    dict_c['UserName'] = i['name']  # 用户姓名
                    dict_c['UserAbbrname'] = i['abbrname']  # 用户简称
                    dict_c['SortCode'] = int(i['sort_code'])  # 所属分类码
                    dict_c['CcusexchName'] = i['ccusexch_name']  # 币种
                    dict_c['Bcusdomestic'] = i['bcusdomestic']  # 国内
                    dict_c['Bcusoverseas'] = i['bcusoverseas']  # 国外
                    dict_c['Bserviceattribute'] = i['bserviceattribute']  # 服务
                    dict_c['Ccusmngtypecode'] = i['ccusmngtypecode']  # 客户管理类型
                    dict_c['Ccusmngtypename'] = i['ccusmngtypename']  # 客户管理类型名称
                    if 'bank_open' in i:
                        dict_c['BankOpen'] = i['bank_open']  # 开户行
                    if 'bank_acc_number' in i:
                        dict_c['BankAccNumber'] = i['bank_acc_number']  # 银行账号
                    if 'address' in i:
                        dict_c['Address']=i['address']
                    if 'contact' in i:
                        dict_c['Contact'] = i['contact']  # 联系人
                    #考虑手机号和电话的情况
                    if 'mobile' not in i and 'phone' not in i:
                        dict_c['name']="+86 18175368569"
                    if 'mobile' in i or 'phone' in i:
                        if 'mobile' in i and 'phone' in i:
                            if i['mobile'] and i['phone']:
                                if i['mobile'] == i['phone']:
                                    if len(i['mobile']) == 11:
                                        dict_c['name']="+86 "+i['mobile']
                                    elif len(i['mobile']) == 12 and "-" in i['mobile']:
                                        dic = i['phone'].split("-")
                                        dict_c['name'] = "+86 " + dic[0] + dic[1]
                                    elif len(i['mobile'])>11 and "-" not in i['mobile']:
                                        dict_c['name']="+86 15152639874"
                                        dict_c['Remarks']=i['mobile']

                                elif  i['mobile'] != i['phone']:
                                    if len(i['mobile'])==11:
                                        if len(i['phone']) == 11:
                                            dict_c['Tel'] = "86 "+i['phone']
                                        elif len(i['phone']) == 12 and "-" in i['phone']:
                                            dic = i['phone'].split("-")
                                            dict_c['Tel'] = "+86 " + dic[0] + dic[1]
                                        elif len(i['phone']) >= 12:
                                            dict_c['Remarks'] = i['phone']
                                        dict_c['name'] = "+86 " + i['mobile']
                                    elif len(i['mobile']) > 11:
                                        if len(i['phone']) == 11:
                                            dict_c['Tel'] = "+86 "+i['phone']
                                        elif len(i['phone']) == 12 and "-" in i['phone']:
                                            dic = i['phone'].split("-")
                                            dict_c['Tel'] = "+86 " + dic[0] + dic[1]
                                        elif len(i['phone']) >= 12:
                                            dict_c['Remarks'] = i['phone']
                                        aa='(13\d|14[5|7]|15\d|166|17[3|6|7]|18\d)\d{8}'
                                        dit =re.search(aa, i['mobile']).group()
                                        dict_c['name']='+86 '+ dit
                                        dict_c['Remarks']=i['mobile']

                            elif i['phone'] and not i['mobile'] :
                                phone(dict_c,i['phone'])
                            elif i['mobile'] and not i['phone']:
                                mobile(dict_c, i['mobile'])

                        elif 'mobile' in i and 'phone' not in i:
                            if i['mobile']:
                                mobile(dict_c,i['mobile'])
                            if not i['mobile']:
                                dict_c['name']="+86 18175368569"
                        elif 'mobile' not in i and 'phone' in i:
                            if i['phone']:
                                phone(dict_c, i['phone'])
                            if not i['phone']:
                                dict_c['name'] = "+86 18175368569"
                    if 'devliver_site' in i:
                        dict_c['DevliverSite'] = i['devliver_site']  # 发货地址
                    if 'spec_operator' in i:
                        dict_c['SpecOperator'] = i['spec_operator']  # 专管业务员编码
                    if 'spec_operator_name' in i:
                        dict_c['SpecOperatorName'] = i['spec_operator_name']  # 专管业务员名称
                    list_c.append(dict_c)
                payload = {"objects": list_c}
                post_meiqia(payload, url)

            elif key == 'saleorderlist':#订单信息
                url = "/api/v1.0/one/OrderInfo/"
                data = value['saleorderlist']
                list_s=[]
                for i in data:
                    dict_s = {}
                    dict_s['name'] = i['code']  # 订单号
                    dict_s['OrderTime'] = i['date'] + "T00:00:00Z"  # 日期
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
                    dict_s['Dpremodatebt'] = i['dpremodatebt'] + "T15:04:05Z"  # 预完工日期
                    dict_s['Dpredatebt'] = i['dpredatebt'] + "T15:04:05Z"  # 预发货日期
                    dict_s['Maker'] = i['maker']  # 制单人
                    dict_s['Money'] = float(i['money'])  # 无税金额
                    dict_s['Sum'] = float(i['sum'])  # 价税合计
                    if 'createsystime' in i:#系统创建时间
                        dict_s['Createsystime']=i['createsystime'].split(" ")[0] + "T" + \
                                           i['createsystime'].split(" ")[1].split(".")[0] + "Z"
                    if 'verifysystime' in i:
                        dict_s['Verifysystime']=i['verifysystime'].split(" ")[0] + "T" + \
                                           i['verifysystime'].split(" ")[1].split(".")[0] + "Z"
                    if 'verifier' in i:
                        dict_s['Verifier'] = i['verifier']  # 审核人
                    if 'define14' in i:
                        dict_s['Define14'] = i['define14']  # 地址
                    if 'fhstatus' in i:  # 发货状态(0=未发货;1=部分发货;2=全部发货)
                        if i['fhstatus'] == "0":
                            dict_s['Fhstatus'] = "未发货"
                        elif i['fhstatus'] == "1":
                            dict_s['Fhstatus'] = "部分发货"
                        else:
                            dict_s['Fhstatus'] = "全部发货"
                    list_s.append(dict_s)
                payload={"objects":list_s}
                post_meiqia(payload, url)

            elif key == 'inventory':# 库存货信息
                url = "/api/v1.0/one/Product/"
                data = value['inventory']
                list_i = []
                for i in data:
                    dict_i = {}
                    dict_i['ProductNumber'] = i['code']  # 产品编码
                    dict_i['name'] = i['name']  # 存货名称
                    if "specs" in i:
                        dict_i['Specs'] = i['specs']  # 规格型号
                    dict_i['ProductSortCode'] = i['sort_code']  # 所属分类码
                    dict_i['ProductSortName'] = i['sort_name']  # 所属分类名称
                    dict_i['MainMeasure'] = i['main_measure']  # 主计量单位
                    dict_i['Unit'] = i['ccomunitname']  # 单位
                    dict_i['Imptaxrate'] = float(i['iimptaxrate'])/100  # 进项税率
                    dict_i['TaxRate'] = float(i['tax_rate'])/100  # 销售税率
                    dict_i['StartDate'] = i['start_date'].split(" ")[0] + "T" + \
                                          i['start_date'].split(" ")[1].split(".")[0] + "Z"  # 启用时间
                    if 'modifydate' in i:
                        dict_i['ModifyDate'] = i['modifydate'].split(" ")[0] + "T" + \
                                           i['modifydate'].split(" ")[1].split(".")[0] + "Z"  # 变更时间
                    if 'isupplytype' in i:
                        dict_i['ProductIsupplyType'] = i['isupplytype']  # 供应类型

                    if 'ref_sale_price' in i:
                        dict_i['Price']=i['ref_sale_price']#单价
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
                        dict_i['Entry'] = i['entry'][0]['invcode']  # 存货编码
                    list_i.append(dict_i)
                payload = {"objects": list_i}
                post_meiqia(payload, url)

            self.data_queue.task_done()


def main():

    # 批量获取客户信息
    page_index = '1'
    #设置时间
    # start_date="2018-09-1720:30:00.0"
    # end_date="2018-09-1721:30:00.0"
    # 前一天时间
    # timestamp_begin = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%Y-%m-%d%H:%M:%S")+".0"  # 昨天零点
    # timestamp_end = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%Y-%m-%d") + '23:59:59.0'  # 昨天23:59:59
    # end_url = 'from_account=bolebaokaifa&timestamp_begin='+timestamp_begin+'&timestamp_end='+timestamp_end+'&to_account=bolebao&app_key=opa87ad77a2a44f12df&token=' + \
    #     token + '&page_index=' + page_index + '&rows_per_page=20&ds_sequence=1'

    end_url = 'from_account=bolebaokaifa&to_account=bolebao&app_key=opa87ad77a2a44f12df&token=' + \
        token + '&page_index=' + page_index + '&rows_per_page=20&ds_sequence=1'

    # 销售订单信息
    order_url = 'https://api.yonyouup.com/api/saleorderlist/batch_get?' + end_url
    # 客户信息
    customer = 'https://api.yonyouup.com/api/customer/batch_get?' + end_url

    # 库存货信息
    inventory = 'https://api.yonyouup.com/api/inventory/batch_get?' + end_url

    list = [order_url]

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

    for i in range(4):
        try:
            logger.info('开启线程获取queue数据')
            t = ThreadData(data_queue)
            t.setDaemon(True)
            t.start()
        except Exception as error:
            logger.error('开启线程请求queue异常')
            # print(error)
    time.sleep(4)

    url_queue.join()
    data_queue.join()



if __name__ == '__main__':
    main()
