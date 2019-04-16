import json
from suds.client import Client
from urllib import request,parse
import numpy

def analy_date(date):
    list_a =[]
    n = 0
    i = 2000
    while True:
        list_a.append(date[n:i])
        n += 2000
        i += 2000
        if n >= len(date):
            break
    return list_a
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
        print(error)
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
            print(self.url)
            req = request.Request(url = self.url, headers = self.header)
            res = request.urlopen(req)
            res = res.read().decode(encoding='utf-8')
            red = json.loads(res)
            if red['code'] == 0:
                return red['body']['objects']
            else:
                return None
        except Exception as error:
            print('获取ID时报错，错误为:%s,url为:%s'%(error,self.url))
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
            print('执行新增时报错，报错为:%s'%error)

# get_url = 'https://crm.meiqia.com/api/v1.0/one/dsl/query?dsl={"SN":{"fields":["id","name"],"cond":{"in":{"name":['+'"D06-AAA4A007045","D06-AAA4A025432"'+']}}}}'
# print(get_url)
# method = Method(get_url).get_id()
# print(method)
# ls1 = ['D06-AAA4A007045','D06-AAA4A025432']
# str1 = ''
# for i in ls1:
# 	str1 = str1 +'"'+ i + '"'+','
# print(str1)
# ls2 = str1[:-1].split(',')
# for i in ls2:
#     print(i)
# get_url = 'https://crm.meiqia.com/api/v1.0/one/dsl/query?dsl={"SN":{"fields":["id","name"],"cond":{"in":{"name":["D06-AAA4A007045","D06-AAA4A025432"]}}}}'
# # get_url = 'https://crm.meiqia.com/api/v1.0/one/dsl/query?dsl={"SN":{"fields":["id","name"],"cond":{"in":{"name":[ '+str()+']}}}}'
# method = Method(get_url).get_id()
# print(method)

def web_date(object_name,date):
    date_sn = list(date.keys())
    url = 'https://crm.meiqia.com/api/v1.0/one/dsl/query?dsl={"'+object_name+'":{"fields":["id","name"],"cond":{"in":{"name":'+ parse.quote(date_sn) +'}}}}'
aa='"C02R500AA014BD000135","B20A150AA014CF009620","B04-R50AAA4B033076","D06AAAAAA044BQ003162","B04-R50AAA4B033078","H1AAAAAAA034CA031091","D06AAAAAA044BQ000794","C02R500AA014BD000495","C02R500AA014BD001220","B02-R50AAA4B031681","M06AAAAAA044AE007030","H1AAAAAAA034CA032867","B04-R50AAA4B033092","D06AAAAAA044BQ003229","C12N500AA0149H000300","D06AAAAAA044BQ004172","B05-R75AAA4BF32373","B05-R75AAA4BF32357","C12N500AA0149H000335","B05-R75AAA4BF32358","B20A150AA014CF011415","B05-R75AAA4BF32366","B05-R75AAA4BF32365","B05-R75AAA4BF32355","H4AAAAAAA034BL007993","B20A150AA014CF011575","S22-A700AA46000545","H4AAAAAAA034BL001142","H4AAAAAAA034BL001137","H4AAAAAAA034BL001122","B20A150AA014CD000020","M06AAAAAA044AE007294","H1AAAAAAA034CA031387","B04-R50AAA4B033074","B04-R50AAA4B033080","B04-R50AAA4B033084","H1AAAAAAA034CA031392","B05-R75AAA4BF32364","H1AAAAAAA034CA031086","H1AAAAAAA034CA031372","B04-R50AAA4B033071","B04-R50AAA4B033095","M06AAAAAA044AE007102","H1AAAAAAA034CA032847","B04-R50AAA4B033073","B20A150AA014CD000040","H1AAAAAAA034CA032852","B20A150AA014CD000235","M06AAAAAA044AE007801","C02R500AA014BD000295","B20A150AA014CF011500","B20A150AA014CF008960","D04AAAAAA044BQ002224","H1AAAAAAA034CA031071","H4AAAAAAA034BL008000","B02-R50AAA4B031714","D04AAAAAA044BK000714","C02R500AA014BD000215","B20A150AA014CF009115","B20A150AA014CF008775","B05-R75AAA4BF32378","D06AAAAAA044BQ001090"'
lis = []
for i in aa.split(','):
    lis.append(i)
print(set(aa))