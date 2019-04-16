# -*- coding:utf-8 -*-
import json
import time
import logging
import os
import copy
from urllib import request,parse

public_url = ''
#log
def loger():
    root_path = os.getcwd()
    log_path = root_path + '/Logs'
    exist_file = os.path.exists(log_path)
    if not exist_file:
        os.makedirs(log_path)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
    log_path = log_path + '/'

    log_name = log_path + rq + '.log'
    logfile = log_name
    fh = logging.FileHandler(logfile, mode='w', encoding='utf-8')
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger


#http请求
class Methods:

    def __init__(self,url,payload=None):
        self.url = url
        self.payload = payload
        self.header = {
        'x-token': "AT13A0MvLFwAAEFRQUNRcXdlWkFZQkFBQUFMYVVETFVaVFV4VXZxZ0VBQVFBQ1Fxd2VYUkVCQUFBQTM1eDc2WkhsTEJVWXBRQUGqmf7P_Lopu4G8R8wQUwZSJwWGdI7JW_ML9DCJe5XqOxr3W4TnNGGY4F1ZyfPrVkJOlwmwCGVFm3p4YDoXxQiJ",
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

            loger().info('获取ID时报错，错误为:%s,url为:%s'%(error,self.url))

    def post_data(self):
        try:

            textmod = json.dumps(self.payload).encode(encoding='utf-8')
            client = request.Request(url=self.url,data=textmod,headers=self.header)
            client_data = request.urlopen(client)
            client_json = json.loads(client_data.read().decode(encoding='utf-8'))
            print(client_json)
            if client_json['code'] == 0:
                print('插入成功!!')
                return client_json['body'][0]['id']
            else:
                print('插入失败!!')
                loger().info('插入失败,url为：%s原数据为：%s'%(self.url,self.payload))
                return None

        except Exception as error:
            print('报错!!!!!')
            loger().info('执行新增时报错，报错信息为：%s' %error)
            return None
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
            get_id = Methods(url).get_id()
            if get_id :
                record_id = get_id['body']['objects']
                if record_id:
                    return record_id

            else:
                if i == 3:
                    return None
            i += 1

#将数据分为200个一份
def group_data(data):

    new_list = []
    start_num = 0
    end_num = 200

    while True:
        new_list.append(data[start_num:end_num])
        start_num += 200
        end_num += 200
        if start_num >= len(data):
            break
    return new_list
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

    data = data
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

                record_id = Methods(get_url).get_id()

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

                record_id = Methods(get_url).get_id()

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


