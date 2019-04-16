#!/usr/bin/python3
from urllib import parse,request
import pymysql
import json
#连接数据库，将数据写到本地文件
def connect_db(date):

    try:

        db = pymysql.connect(host="10.100.7.148",port=13011, user="yf_read", passwd="yf_read@123", db="AQACQqweXREBAAAA35x76ZHlLBUYpQAA",charset="utf8")

        cursor = db.cursor()

        cursor.execute("select id,name from %s where is_deleted=0"%date)

        data = cursor.fetchall()
        if data:
            with open('%s.txt'%date,'w') as f:
                for i in data:
                    if len(i) == 1:
                        print(i)
                    f.write(str(i))
                    f.write('\n')

        db.close()
    except:
        print("出错")
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
            print('获取ID时报错，错误为:%s,url为:%s'%(error,self.url))

#读文件，处理文件内容
def read_file(obj,date):

    with open('%s.txt'%obj) as f:
        while True:
            content = f.readline().rstrip()
            if not content:
                break
            record = content.split(' ')
            if date == record[1]:

                return record[0]
        return None
# import time
#
# aa = time.time()
# url = 'https://crm.meiqia.com/api/v1.0/one/dsl/query?dsl={"OrderInfo":{"fields":"name","cond":{"in":{"id":["AQACQqweGRMBAAAA--4628Z_aBVODAIA","AQACQqweGRMBAAAA--4pAuR_aBVKDgIA","AQACQqweGRMBAAAA--4tb6d_aBWKCgIA","AQACQqweGRMBAAAA--7DGGZ9aBXj5gEA","AQACQqweGRMBAAAA--7DGGZ9aBXj5gEA","AQACQqweGRMBAAAA--KnpN1-aBWi_gEA"]}}}}'
# print(Method(url).get_id())
# print(time.time()-aa)
# def data_processing(date):
