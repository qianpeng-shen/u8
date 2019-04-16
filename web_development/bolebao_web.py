# encoding=utf-8
import json
import os
import logging
import time
import datetime
import http.client

from urllib import parse,request
from suds.client import Client

from web import read_file,connect_db

root_path = os.getcwd()
log_path = root_path + '/Logs'
exist_file = os.path.exists(log_path)
if not exist_file:
    os.makedirs(log_path)

logger = logging.getLogger()
logger.setLevel(logging.INFO)
rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
log_path = os.path.dirname(os.getcwd()) + '/web_project/Logs/'

log_name = log_path + rq + '.log'
logfile = log_name
fh = logging.FileHandler(logfile, mode='w', encoding='utf-8')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
fh.setFormatter(formatter)
logger.addHandler(fh)

sn={}

class Method():
    def __init__(self,url,payload = None):
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
            req = request.Request(url = self.url, headers = self.header)
            res = request.urlopen(req)
            res = res.read().decode(encoding='utf-8')
            red = json.loads(res)

            if red['code'] == 0 :
                return red
            else:
                return None
        except Exception as error:
            logger.info('获取ID时报错，错误为:%s,url为:%s'%(error,self.url))

    def post_date(self):
        try:
            print("插入数据")
            textmod = json.dumps(self.payload).encode(encoding='utf-8')
            req = request.Request(url = self.url, data = textmod, headers = self.header)
            res = request.urlopen(req)
            res = res.read().decode(encoding='utf-8')
            res_data = json.loads(res)
            print(res_data)
        except Exception as error:
            logger.info('执行新增时报错，报错为:%s'%error)

    def put_date(self):
        try:
            print("修改数据")
            conn = http.client.HTTPSConnection("crm.meiqia.com")#连接指定的服务器
            payload = json.dumps(self.payload)

            conn.request(method = "PUT", url = self.url, body = payload, headers = self.header)#使用指定的方法和url向服务器发送请求

            res = conn.getresponse()#返回一个 HTTPResponse 实例
            data = res.read().decode("utf-8")#读取内容

            data=json.loads(data)
            print(data)

            conn.close()
        except Exception as error:
            logger.info('执行更新数据时报错，报错为:%s' %error)

#期初同步webservice中的数据
def query_insert(date):
	global sn
	date_sn = date['name']
	if date['name'] in sn.keys():
		sn_key = sn[date_sn]
		if date['ddatetime']>sn_key['ddatetime']:
			sn[date_sn] = date
	else:
		sn[date['name']] = date

#解决get_id获取时失败的情况
def get_date(url,date):
	url = url
	if date:
		date_id = date['body']['objects']
		if date_id:
			return date_id[0]['id']
		else:
			return None
	else:
		i = 1
		while i <= 3:
			get_id = Method(url).get_id()
			if get_id :
				record_id = date['body']['objects']
				if record_id:
					return record_id[0]['id']
				else:
					return None
			else:
				if i == 3:
					return None
			i += 1
#连接webservice接口
def get_webdata():
    url = 'http://124.207.40.126:9000/b888/TTSWebDataAccess.asmx?WSDL'
    client = Client(url)

    time_begin = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
    time_end = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%Y-%m-%d") + ' 23:59:59'
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
          "ddatetime": "BETWEEN '%s' and '%s'"
        }
      }
    }''' %(time_begin, time_end)

    faceName = "querybddoc"
    try:
        res = client.service.GetWebDataForJson(innerJson=innerJson, faceName=faceName)
        data = json.loads(res)
        return data

    except Exception as error:
        logger.error(error)

#将获取到的数据通过解析进行新增获更新操作
def analytical_data(receive):

    data = receive['datafromnc']['billinfos']
    if data:
        for i in data['billinfo']:
            list_d = {}
            remarks = ''
            list_d['ccode'] = i['ccode']#单据号
            list_d['sixNineCode'] = i['barcode69']#69码
            list_d['ProductNumber'] = i['cinvcode']#商品编码
            if i['ddatetime']:
                ddatetime = i['ddatetime'].split(" ")
                list_d['ddatetime'] = ddatetime[0] + "T" + ddatetime[1] + "Z"#时间戳
            list_d['operatorName'] = i['cmaker']#操作人
            if i['rkdate']:
                list_d['inStorageTime'] = i['rkdate'] + "T00:00:00Z"#入库时间
            if i['ckdate']:
                list_d['outStorageTime'] = i['ckdate'] + "T00:00:00Z"#出库时间
            if i['cinvcode']:
                url = 'https://crm.meiqia.com/api/v1.0/one/dsl/query?dsl={"Product":{"fields":"id","cond":{"==":{"ProductNumber":"' + parse.quote(i['cinvcode']) + '"}}}}'
                product = Method(url).get_id()
                product = product['body']['objects']
                if product :
                    list_d['ProductID'] = product[0]['id']#通过编码返回商品名称id
                else:
                    remarks = remarks + '商品编码:' + i['cinvname'] + ';'
            list_d['Specs'] = i['cinvstd']#规格型号
            list_d['name'] = i['snno']#sn
            list_d['State'] = i['snstate']#sn状态
            list_d['operateType'] = i['itype']#类型
            list_d['StorageName'] = i['cwhname']#仓库名称
            if i['csocode']:
                url = 'https://crm.meiqia.com/api/v1.0/one/dsl/query?dsl={"OrderInfo":{"fields":"id","cond":{"==":{"name":"' + parse.quote(i['csocode']) + '"}}}}'
                order = Method(url).get_id()
                order = order['body']['objects']
                if order:
                    list_d['OrderInfoID'] = order[0]['id']#销售订单号
                else:
                    remarks = remarks + '订单号:' + i['csocode'] + ';'
            if i['qd']:
                url = 'https://crm.meiqia.com/api/v1.0/one/dsl/query?dsl={"Channel":{"fields":"id","cond":{"==":{"name":"' + parse.quote(i['qd']) + '"}}}}'
                chanel = Method(url).get_id()
                chanel = chanel['body']['objects']
                if chanel :
                    list_d['ChannelID'] = chanel[0]['id']#渠道
                else:
                    remarks = remarks + '渠道:' + i['qd'] + ';'
            list_d['remarks'] = remarks

            query_insert(list_d)


#格式处理后，进行修改或新增
def cond(data,cond_sn):
    global sn
    cond_sn = cond_sn
    get_url = 'https://crm.meiqia.com/api/v1.0/one/dsl/query?dsl={"SN":{"fields":["id","name"],"cond":{"in":{"name":['+ data +']}},"limit":500}}'
    cond_id = get_date(get_url,Method(get_url).get_id())
    print(cond_id,"0000")

    # if cond_id :
    #
    #     cond_dict = {}
    #     print("修改",len(cond_id),"条数据")
    #     for i in cond_id:
    #         cond_dict[i['name']] = i['id']
    #         put_url = '/api/v1.0/one/SN/' + i['id']
    #         cond_date = sn[i['name']]
    #         cond_date['version'] = i['version']
    #         Method(put_url,cond_date).put_date()
    #     cond_list = list(set(cond_sn).difference(set(list(cond_dict.keys()))))
    #
    #     if len(cond_list) != 0:
    #         print("新增",len(cond_list),"条数据")
    #         for i in cond_list:
    #
    #             post_url = "https://crm.meiqia.com/api/v1.0/one/SN/"
    #             Method(post_url,{'objects':[sn[i]]}).post_date()
    #
    # else:
    #     print("新增",len(cond_sn),"条数据")
    #     for i in cond_sn:
    #         post_url = "https://crm.meiqia.com/api/v1.0/one/SN/"
    #         Method(post_url,{'objects':[sn[i]]}).post_date()

#将增量数据进行格式处理
def sn_name(date):

    date_sn = list(date.keys())
    str_sn1 = ''
    sn_num = len(date_sn)

    if sn_num <= 200:
        for i in date_sn:
            str_sn1 = str_sn1 + '"' + i + '"' + ','
        cond(str_sn1[:-1],date_sn)
    else:
        num = sn_num // 200
        for i in range(num+1):
            str_sn2 = ''
            for i in date_sn[i*200:(i+1)*200]:
                str_sn2 = str_sn2 + '"' + i + '"' + ','
            if len(str_sn2) != 0:
                cond(str_sn2[:-1],date_sn[i*200:(i+1)*200])
#主程序
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
    print(sn)
    sn_name(sn)

if __name__ == '__main__':
    main()

