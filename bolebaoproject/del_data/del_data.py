# -*- coding:utf-8 -*-
import json
import http.client
from urllib import request
class Method():

    def __init__(self,url,payload = None):

        self.url = url
        self.payload = payload
        self.header = {'x-token':'AT13A0MvLFwAAEFRQUNRcXdlWkFZQkFBQUFMYVVETFVaVFV4VXZxZ0VBQVFBQ1Fxd2VYUkVCQUFBQTM1eDc2WkhsTEJVWXBRQUGqmf7P_Lopu4G8R8wQUwZSJwWGdI7JW_ML9DCJe5XqOxr3W4TnNGGY4F1ZyfPrVkJOlwmwCGVFm3p4YDoXxQiJ','content-type':'application/json'}

    def get_id(self):

        try:

            req = request.Request(url = self.url, headers = self.header)
            res = request.urlopen(req)
            res = res.read().decode(encoding='utf-8')
            red = json.loads(res)

            if red['code'] == 0 :
                return red['body']['objects']
            else:
                return None
        except Exception as error:

            print('获取ID时报错，错误为:%s,url为:%s'%(error,self.url))

    def post_data(self):

        try:
            print('post')
            textmod = json.dumps(self.payload).encode(encoding='utf-8')
            req = request.Request(url = self.url, data = textmod, headers = self.header)

            res = request.urlopen(req)

            res = res.read().decode(encoding='utf-8')
            res_data = json.loads(res)
            print(res_data)

        except Exception as error:

            print('执行新增时报错，报错为:%s'%error)

    def put_data(self):

        try:

            print('put')

            conn = http.client.HTTPSConnection('crm.meiqia.com')
            payload = json.dumps(self.payload)

            conn.request(method = "PUT", url = self.url, body = payload, headers = self.header)#使用指定的方法和url向服务器发送请求

            res = conn.getresponse()#返回一个 HTTPResponse 实例
            data = res.read().decode("utf-8")#读取内容

            data=json.loads(data)
            print(data)

            conn.close()

        except Exception as error:

            print('执行更新数据时报错，报错为:%s' %error)
    def del_data(self):

        try:

            conn = http.client.HTTPConnection('10.82.2.29','7010')
            payload = json.dumps(self.payload)
            conn.request("DELETE", url = self.url,body=payload, headers = self.header)
            res = conn.getresponse()
            data = res.read().decode("utf-8")

            data = json.loads(data)
            print(data)

            conn.close()
        except Exception as error:
            print('删除信息时报错，报错为%s' %error)
def delete_data(object_name):

    while True:

        revise_url = 'https://crm.meiqia.com/api/v1.0/one/dsl/query?dsl={"SN":{"fileds":"id","limit":500}}'
        return_id = Method(revise_url).get_id()

        del_list = []
        if return_id:
            for i in return_id:
                # two_url = '/api/v1.0/one/'+object_name+'/'+i['id']+'/?version='+str(i['version'])
                # Method(two_url).del_data()
                del_dict = {}
                del_dict["object_id"] = i['id']
                del_dict["version"] = i['version']
                del_list.append(del_dict)

            two_url = '/api/v1.0/one/'+object_name+'/object_list'

            Method(two_url,{"objects":del_list}).del_data()
        else:
            break

if __name__ == '__main__':
    object_name = 'SN'
    delete_data(object_name)