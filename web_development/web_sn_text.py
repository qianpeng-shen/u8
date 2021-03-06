# encoding=utf-8
import json
import os
import logging
import time
import http.client

from urllib import parse, request
from suds.client import Client
from public_method import analy_data
root_path = os.getcwd()
log_path = root_path + '/Logs'
exist_file = os.path.exists(log_path)
if not exist_file:
    os.makedirs(log_path)

logger = logging.getLogger()
logger.setLevel(logging.INFO)
rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
log_path = os.path.dirname(os.getcwd()) + '/web_development/Logs/'

log_name = log_path + rq + '.log'
logfile = log_name
fh = logging.FileHandler(logfile, mode='w', encoding='utf-8')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
fh.setFormatter(formatter)
logger.addHandler(fh)

sn = {}


class Method():
    def __init__(self, url, payload=None):
        self.url = url
        self.payload = payload
        self.header = {
            'x-token': "AT13A0MvLFwAAEFRQUNRcXdlWkFZQkFBQUFMYVVETFVaVFV4VXZxZ0VBQVFBQ1Fxd2VYUkVCQUFBQTM1eDc2WkhsTEJVWXBRQUGqmf7P_Lopu4G8R8wQUwZSJwWGdI7JW_ML9DCJe5XqOxr3W4TnNGGY4F1ZyfPrVkJOlwmwCGVFm3p4YDoXxQiJ",
            'content-type': "application/json",
            'cache-control': "no-cache",
            'postman-token': "529a9a27-2e62-0d64-aea9-c938d33ec5fd"
        }

    def get_id(self):
        try:
            req = request.Request(url=self.url, headers=self.header)
            res = request.urlopen(req)
            res = res.read().decode(encoding='utf-8')
            red = json.loads(res)

            if red['code'] == 0:
                return red['body']['objects']
            else:
                return None
        except Exception as error:
            logger.info('获取ID时报错，错误为:%s,url为:%s' % (error, self.url))

    def post_date(self):
        try:
            print("插入数据")
            textmod = json.dumps(self.payload).encode(encoding='utf-8')
            req = request.Request(url=self.url, data=textmod, headers=self.header)
            res = request.urlopen(req)
            res = res.read().decode(encoding='utf-8')
            res_data = json.loads(res)
            print(res_data)
        except Exception as error:
            logger.info('执行新增时报错，报错为:%s' % error)

    def put_date(self):
        try:
            conn = http.client.HTTPSConnection("crm.meiqia.com")  # 连接指定的服务器
            payload = json.dumps(self.payload)

            conn.request(method="PUT", url=self.url, body=payload, headers=self.header)  # 使用指定的方法和url向服务器发送请求

            res = conn.getresponse()  # 返回一个 HTTPResponse 实例
            data = res.read().decode("utf-8")  # 读取内容

            data = json.loads(data)
            print(data)

            conn.close()
        except Exception as error:
            logger.info('执行更新数据时报错，报错为:%s' % error)


# 期初同步webservice中的数据
def query_insert(data):

    global sn
    date_sn = data['name']
    if data['name'] in sn.keys():
        sn_key = sn[date_sn]
        if data['ddatetime'] > sn_key['ddatetime']:
            sn[date_sn] = data
    else:
        sn[data['name']] = data


# 连接webservice接口
def get_webdata():
    url = 'http://124.207.40.126:9000/b888/TTSWebDataAccess.asmx?WSDL'
    client = Client(url)
    innerJson = '''{
      "datafromnc": {
        "nccontext": {
          "user": "mq",
          "password": "123",
          "exsystemcode": "BarCode99",
          "doctype": "INVSN2CRM"
        },
        "queryinfos": {
          "snno": "",
          "ddatetime": ""
        }
      }
    }'''

    faceName = "querybddoc"
    try:
        res = client.service.GetWebDataForJson(innerJson=innerJson, faceName=faceName)
        data = json.loads(res)
        return data

    except Exception as error:
        logger.error(error)


# 将获取到的数据通过解析进行新增获更新操作
def analytical_data(receive):
    data = receive['datafromnc']['billinfos']
    if data:
        for i in data['billinfo']:
            list_d = {}
            remarks = ''
            list_d['ccode'] = i['ccode']  # 单据号
            list_d['sixNineCode'] = i['barcode69']  # 69码
            list_d['ProductNumber'] = i['cinvcode']  # 商品编码
            if i['ddatetime']:
                list_d['ddatetime'] = str(time.mktime(time.strptime(i['ddatetime'],"%Y-%m-%d %H:%M:%S"))) # 时间戳
            list_d['operatorName'] = i['cmaker']  # 操作人
            if i['rkdate']:
                list_d['inStorageTime'] = i['rkdate'] + "T00:00:00Z"  # 入库时间
            if i['ckdate']:
                list_d['outStorageTime'] = i['ckdate'] + "T00:00:00Z"  # 出库时间
            if i['cinvcode']:
                url = 'https://crm.meiqia.com/api/v1.0/one/dsl/query?dsl={"Product":{"fields":"id","cond":{"==":{"ProductNumber":"' + parse.quote(
                    i['cinvcode']) + '"}}}}'
                product = Method(url).get_id()
                if product:
                    list_d['ProductID'] = product[0]['id']  # 通过编码返回商品名称id
                else:
                    remarks = remarks + '商品编码:' + i['cinvname'] + ';'
            list_d['Specs'] = i['cinvstd']  # 规格型号
            list_d['name'] = i['snno'].strip() # sn
            list_d['State'] = i['snstate']  # sn状态
            list_d['operateType'] = i['itype']  # 类型
            list_d['StorageName'] = i['cwhname']  # 仓库名称
            if i['csocode']:
                url = 'https://crm.meiqia.com/api/v1.0/one/dsl/query?dsl={"OrderInfo":{"fields":"id","cond":{"==":{"name":"' + parse.quote(
                    i['csocode']) + '"}}}}'
                order = Method(url).get_id()
                if order:
                    list_d['OrderInfoID'] = order[0]['id']  # 销售订单号
                else:
                    remarks = remarks + '订单号:' + i['csocode'] + ';'
            if i['qd']:
                url = 'https://crm.meiqia.com/api/v1.0/one/dsl/query?dsl={"Channel":{"fields":"id","cond":{"==":{"name":"' + parse.quote(
                    i['qd']) + '"}}}}'
                chanel = Method(url).get_id()
                if chanel:
                    list_d['ChannelID'] = chanel[0]['id']  # 渠道
                else:
                    remarks = remarks + '渠道:' + i['qd'] + ';'
            list_d['remarks'] = remarks

            query_insert(list_d)


# 将数据分为200每份
def analy_data(date):
    list_a = []
    n = 0
    i = 200
    while True:
        list_a.append(date[n:i])
        n += 200
        i += 200
        if n >= len(date):
            break
    return list_a


def main():
    web_data = get_webdata()

    if not web_data:
        i = 1
        while i <= 3:

            web_data = get_webdata()
            if web_data:
                analytical_data(web_data)
                break
            i += 1
    else:
        analytical_data(web_data)
    list_sn = list(sn.values())
    analy_sn = analy_data(list_sn)
    for i in analy_sn:
        url = "https://crm.meiqia.com/api/v1.0/one/SN/"
        Method(url, {'objects': i}).post_date()


if __name__ == '__main__':
    main()

