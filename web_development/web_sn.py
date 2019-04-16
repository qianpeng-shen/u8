# encoding=utf-8
import json
import os
import logging
import time

from suds.client import Client
from public_method import analy_data,Method,cond_data
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
          "ddatetime": "BETWEEN '2018-10-15' and '2018-10-16'"
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
        print(len(data['billinfo']))
        for i in data['billinfo']:

            list_d = {}
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

                list_d['ProductID'] = i['cinvcode']  # 通过编码返回商品名称id
            else:
                 list_d['ProductID'] = "productid"
            list_d['Specs'] = i['cinvstd']  # 规格型号
            list_d['name'] = i['snno'].strip() # sn
            list_d['State'] = i['snstate']  # sn状态
            list_d['operateType'] = i['itype']  # 类型
            list_d['StorageName'] = i['cwhname']  # 仓库名称
            if i['csocode']:

                list_d['OrderInfoID'] = i['csocode']  # 销售订单号
            else:
                list_d['OrderInfoID'] = "orderinfoid"
            if i['qd']:
                list_d['ChannelID'] = i['qd']  # 渠道
            else:
                list_d['ChannelID'] = "channelid"


            query_insert(list_d)


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
    info_list = [['OrderInfo','OrderInfoID'],['Channel','ChannelID'],['Product','ProductID','ProductNumber','ProductNumber']]
    list_sn = list(sn.values())
    for i in info_list:
        list_sn = cond_data(list_sn, i)
    print(list_sn)
    # analy_sn = analy_data(list_sn)
    # for i in analy_sn:
    #     url = "https://crm.meiqia.com/api/v1.0/one/SN/"
    #     Method(url, {'objects': i}).post_data()


if __name__ == '__main__':
    main()

