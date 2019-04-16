# -*- coding:utf-8 -*-
import json
import datetime

from suds.client import Client

from public_methods import loger,get_record,cond_data

sn={}

#期初同步webservice中的数据
def query_insert(data):

    global sn
    data_sn = data['name']
    if data['name'] in sn.keys():
        sn_key = sn[data_sn]
        if data['ddatetime']>sn_key['ddatetime']:
            sn[data_sn] = data
    else:
        sn[data['name']] = data


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
    }''' %(time_begin,time_end)


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
            if 'cinvcode' in i:
                if i['cinvcode']:
                    list_d['ProductID'] = i['cinvname']

            list_d['Specs'] = i['cinvstd']#规格型号
            list_d['name'] = i['snno'].strip()#sn
            list_d['State'] = i['snstate']#sn状态
            list_d['operateType'] = i['itype']#类型
            list_d['StorageName'] = i['cwhname']#仓库名称
            if i['csocode']:
                list_d['OrderInfoID'] = i['csocode']

            if i['qd']:
                list_d['ChannelID'] = i['qd']
            if 'ProductID' not in list_d:
                list_d['ProductID'] = 'productida'
            if 'OrderInfoID' not in list_d:
                list_d['OrderInfoID'] = 'productida'
            if 'ChannelID' not in list_d:
                list_d['ChannelID'] = 'channelida'

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

        info_list = [['OrderInfo','OrderInfoID'],['Channel','ChannelID'],['Product','ProductID','ProductNumber','ProductNumber']]
        sn_values = sn

        for i in info_list:

            sn_values = cond_data(sn_values,i,'name')
        print(sn_values)

        # if sn_values:
        #
        #     get_record(sn_values,'SN','name')
def sn_main():
    main()
if __name__ == '__main__':
    main()

