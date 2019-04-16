# encoding=utf-8

import os
import logging
import time
import json
import http.client
import copy

from urllib import request,parse

# 创建日志文件
def loger():

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
    return logger

class Method():

    def __init__(self,url,payload = None):

        self.url = url
        self.payload = payload
        self.header = {
        'x-token': "AQIAAKhirFwAAEFRQUNRcXdlWGhVQkFBQUFlS0JoNnBIbExCVVAtd0FBQVFBQ1Fxd2VYUkVCQUFBQTM1eDc2WkhsTEJVWXBRQUElvnUJwZtZx5gRRB1ltB3d-2Pt-aaqP39MPttK2wp2_9M9gV1xudnwwx0mBYg2EvjDTAk94BB3u9be-GswMHuk",
        'content-type': "application/json"
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

            loger().info('执行新增时报错，报错为:%s'%error)

    def put_data(self):

        try:
            print("put")
            conn = http.client.HTTPSConnection("crm-test.meiqia.com")#连接指定的服务器
            payload = json.dumps(self.payload)

            conn.request(method = "PUT", url = self.url, body = payload, headers = self.header)#使用指定的方法和url向服务器发送请求

            res = conn.getresponse()#返回一个 HTTPResponse 实例
            data = res.read().decode("utf-8")#读取内容

            data=json.loads(data)
            print(data)

            conn.close()

        except Exception as error:

            loger().info('执行更新数据时报错，报错为:%s' %error)
    def del_data(self):

        try:
            print('del')
            conn = http.client.HTTPSConnection("crm.meiqia.com")
            conn.request("DELETE", url = self.url, headers = self.header)
            res = conn.getresponse()
            data = res.read().decode("utf-8")

            data = json.loads(data)
            print(data)

            conn.close()
        except Exception as Error:
            loger().error(Error)


#解决get_id获取时失败的情况
def get_date(url,date):
    url = url
    if date:

        date_id = date['body']['objects']
        if date_id:
            return date_id
        else:

            return None
    else:
        i = 1
        while i <= 3:

            get_id = Method(url).get_id()

            if get_id :
                record_id = get_id['body']['objects']
                if record_id:
                    return record_id

            else:
                if i == 3:
                    return None
            i += 1

#将数据组成需要的字符串
def analysis_str(record):

    list_data = []
    data_record = record
    str_record1 = ''
    record_num = len(data_record)
    if record_num <= 200:
        for i in data_record:

            str_record1 = str_record1 + '"' + i + '"' + ','
        list_data.append(str_record1[:-1])

    else:
        num = record_num // 200
        for i in range(num+1):
            str_record2 = ''

            for d in data_record[i*200:(i+1)*200]:
                str_record2 = str_record2 + '"' + d + '"' + ','
            if len(str_record2) != 0:

                list_data.append(str_record2[:-1])
    return list_data


# 用dsl获取lookup字段的id,list_data:['表名','替代字段名称','查询字段','表中查询字段']
def cond_data(data,list_data):

    cond_record = []
    order_data = []
    if data:
        #当传入的list_data长度为2时，dsl根据data_name返回name和id
        if len(list_data) == 2:
            obj_name = list_data[0]
            data_name = list_data[1]

            for i in data:
                if data_name in i:
                    cond_record.append(i[data_name])

            for record in analysis_str(cond_record):

                get_url = 'https://crm.meiqia.com/api/v1.0/one/dsl/query?dsl={"' + obj_name + '":{"fields":["id","name"],"cond":{"in":{"name":[' + parse.quote(
                    record) + ']}},"limit":500}}'

                record_id = Method(get_url).get_id()

                cond_id = get_date(get_url, record_id)

                if cond_id:

                    for cond in data:

                        if data_name in cond:
                            if 'sign' in cond:
                                continue
                            for info in cond_id:
                                if cond[data_name] == info['name']:
                                    cond[data_name] = info['id']
                                    temporary_cond = copy.deepcopy(cond)
                                    order_data.append(temporary_cond)

                                    cond['sign'] = '有值'


                            if 'sign' not in cond and cond[data_name] != None:

                                cond[data_name] = None
                                order_data.append(cond)
                else:

                    for cond in data:

                        cond[data_name] = None
                        order_data.append(cond)

        #当list_data 长度为4时，根据参数返回id
        else:

            obj_name = list_data[0]
            data_name = list_data[1]
            query_name = list_data[2]
            query_code = list_data[3]
            #将所需要解析的字段用字符串拼接
            for i in data:
                if data_name in i and query_name in i:
                    cond_record.append(i[query_name])
            #使用dsl中的in方法查询id
            for record in analysis_str(cond_record):

                get_url = 'https://crm.meiqia.com/api/v1.0/one/dsl/query?dsl={"' + obj_name + '":{"fields":["id","' + query_code + '"],"cond":{"in":{"'+ query_code +'":[' + parse.quote(record) + ']}},"limit":500}}'

                record_id = Method(get_url).get_id()

                cond_id = get_date(get_url, record_id)

                if cond_id:

                    for cond in data:

                        if data_name in cond and 'sign' not in cond and cond[data_name] != None:

                            for info in cond_id:
                                if cond[query_name] == info[query_code]:
                                    cond[data_name] = info['id']
                                    temporary_cond = copy.deepcopy(cond)
                                    order_data.append(temporary_cond)
                                    cond['sign'] = '有值'
                                    break


                            if 'sign' not in cond and cond[data_name] != None:
                                cond[data_name] = None
                                order_data.append(cond)
                else:
                    for cond in data:
                        cond[data_name] = None
                        order_data.append(cond)

    return order_data

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
