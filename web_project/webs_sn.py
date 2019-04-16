# -*- coding:utf-8 -*-
import json
import datetime
import time
from urllib import parse
from suds.client import Client

from public_methods import loger,Method,get_record

sn={}

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


#连接webservice接口
def get_webdata():

    url = 'http://124.207.40.126:9000/b888/TTSWebDataAccess.asmx?WSDL'
    client = Client(url)

    time_begin = (datetime.date.today() - datetime.timedelta(days=4)).strftime("%Y-%m-%d %H:%M:%S")
    time_end = (datetime.date.today() - datetime.timedelta(days=4)).strftime("%Y-%m-%d") + ' 23:59:59'
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
    }''' %('2019-03-02 00:00:00', '2019-03-02 23:00:00')


    faceName = "querybddoc"
    try:
        res = client.service.GetWebDataForJson(innerJson=innerJson, faceName=faceName)
        data = json.loads(res)
        return data

    except Exception as error:
        loger().error(error)

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
                list_d['ddatetime'] = str(time.mktime(time.strptime(i['ddatetime'], "%Y-%m-%d %H:%M:%S")))  # 时间戳
            list_d['operatorName'] = i['cmaker']#操作人
            if i['rkdate']:
                list_d['inStorageTime'] = i['rkdate'] + "T00:00:00Z"#入库时间
            if i['ckdate']:
                list_d['outStorageTime'] = i['ckdate'] + "T00:00:00Z"#出库时间
            if i['cinvcode']:
                url = 'https://crm.meiqia.com/api/v1.0/one/dsl/query?dsl={"Product":{"fields":"id","cond":{"==":{"ProductNumber":"' + parse.quote(i['cinvcode']) + '"}}}}'
                product = Method(url).get_id()
                if product :
                    product = product['body']['objects']
                    if product :
                        list_d['ProductID'] = product[0]['id']#通过编码返回商品名称id
                    else:
                        remarks = remarks + '商品编码:' + i['cinvname'] + ';'
                else:
                    remarks = remarks + '商品编码:' + i['cinvname'] + ';'
            list_d['Specs'] = i['cinvstd']#规格型号
            list_d['name'] = i['snno'].strip()#sn
            list_d['State'] = i['snstate']#sn状态
            list_d['operateType'] = i['itype']#类型
            list_d['StorageName'] = i['cwhname']#仓库名称
            if i['csocode']:
                url = 'https://crm.meiqia.com/api/v1.0/one/dsl/query?dsl={"OrderInfo":{"fields":"id","cond":{"==":{"name":"' + parse.quote(i['csocode']) + '"}}}}'
                order = Method(url).get_id()

                if order:
                    order = order['body']['objects']
                    if order:
                        list_d['OrderInfoID'] = order[0]['id']#销售订单号
                    else:
                        remarks = remarks + '订单号:' + i['csocode'] + ';'
                else:
                    remarks = remarks + '订单号:' + i['csocode'] + ';'
            if i['qd']:
                url = 'https://crm.meiqia.com/api/v1.0/one/dsl/query?dsl={"Channel":{"fields":"id","cond":{"==":{"name":"' + parse.quote(i['qd']) + '"}}}}'
                chanel = Method(url).get_id()

                if chanel:
                    chanel = chanel['body']['objects']
                    if chanel:
                        list_d['ChannelID'] = chanel[0]['id']#渠道
                    else:
                        remarks = remarks + '渠道:' + i['qd'] + ';'
                else:
                    remarks = remarks + '渠道:' + i['qd'] + ';'
            list_d['remarks'] = remarks


            query_insert(list_d)


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

    if sn:

        get_record(sn,'SN','name')
def sn_main():
    main()
if __name__ == '__main__':
    main()

