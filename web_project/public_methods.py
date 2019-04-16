# -*- coding:utf-8 -*-

import os

import logging
import time
import json
import copy
import http.client
import configparser
import requests

from urllib import request, parse


cfeat = configparser.ConfigParser()
cfeat.read('./config/config.ini')

public_url = cfeat.get('parameter','public_url')
headers = {'x-token':cfeat.get('parameter','x-token'),'content-type':cfeat.get('parameter','content-type')}
connect_servers = cfeat.get('parameter','connect_servers')
host = ''
if 'crm.meiqia.com' != connect_servers:
    connect = connect_servers.split(':')
    host = connect[0]
    port = int(connect[1])

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

    log_name = log_path + '/' + rq + '.log'
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
        self.header = headers

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

            print('put')
            if host:
                conn = http.client.HTTPConnection(host,port)#连接指定的服务器
            else:
                conn = http.client.HTTPSConnection(connect_servers)
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
            if host:

                conn = http.client.HTTPConnection(host,port)  # 连接指定的服务器
            else:
                conn = http.client.HTTPSConnection(connect_servers)

            conn.request("DELETE", url = self.url, headers = self.header)
            res = conn.getresponse()
            data = res.read().decode("utf-8")

            data = json.loads(data)
            print(data)

            conn.close()
        except Exception as error:
            loger().error('删除信息时报错，报错为%s' %error)


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

#格式处理后，进行修改或新增
def cond(data,cond_record,list_data,obj_name,data_name):

    cond_record = cond_record

    get_url = public_url + '/api/v1.0/one/dsl/query?dsl={"'+ obj_name +'":{"fields":["id","' + data_name + '"],"cond":{"in":{"' + data_name + '":['+ parse.quote(data) +']}},"limit":500}}'
    if 'SN' == obj_name:

        get_url = public_url + '/api/v1.0/one/dsl/query?dsl={"'+ obj_name +'":{"fields":["id","ddatetime","' + data_name + '"],"cond":{"in":{"' + data_name + '":['+ parse.quote(data) +']}},"limit":500}}'

    cond_id = get_date(get_url,Method(get_url).get_id())

    if cond_id :

        cond_dict = {}
        for i in cond_id:

            cond_dict[i[data_name]] = i['id']
            cond_url = '/api/v1.0/one/'+obj_name+'/' + i['id']
            cond_date = list_data[i[data_name]]
            cond_date['version'] = i['version']
            if 'end_time' in cond_date:

                del_url = cond_url + "?version=" + str(cond_date["version"])

                Method(del_url).del_data()
            else:

                if 'ccode' in cond_date and 'ddatetime' in cond_date:

                    if  cond_date['ddatetime'] > i['ddatetime']:

                        Method(cond_url, cond_date).put_data()
                else:

                    Method(cond_url,cond_date).put_data()
        cond_list = list(set(cond_record).difference(set(list(cond_dict.keys()))))

        if len(cond_list) != 0:
            for i in cond_list:
                post_url = public_url + '/api/v1.0/one/'+obj_name+'/'
                if 'end_time' in list_data[i]:
                    continue

                Method(post_url,{'objects':[list_data[i]]}).post_data()

    else:
        for i in cond_record:

            if 'end_time' in list_data[i]:
                continue
            post_url = public_url + '/api/v1.0/one/'+obj_name+'/'

            Method(post_url,{'objects':[list_data[i]]}).post_data()

#将增量数据进行格式处理
def get_record(data,obj_name,data_name):

    data_record = list(data.keys())

    str_record1 = ''
    record_num = len(data_record)
    list_data = data
    if record_num <= 200:
        for i in data_record:
            str_record1 = str_record1 + '"' + i + '"' + ','

        cond(str_record1[:-1],data_record,list_data,obj_name,data_name)
    else:
        num = record_num // 200
        for i in range(num+1):
            str_record2 = ''
            for d in data_record[i*200:(i+1)*200]:
                str_record2 = str_record2 + '"' + d + '"' + ','
            if len(str_record2) != 0:

                cond(str_record2[:-1],data_record[i*200:(i+1)*200],list_data,obj_name,data_name)
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
def cond_data(data,list_data,key_name):

    data = data.values()
    cond_record = []
    order_data = {}
    if data:
        #当传入的list_data长度为2时，dsl根据data_name返回name和id
        if len(list_data) == 2:
            obj_name = list_data[0]
            data_name = list_data[1]

            for i in data:
                if data_name in i:
                    cond_record.append(i[data_name])

            for record in analysis_str(cond_record):

                get_url = public_url + '/api/v1.0/one/dsl/query?dsl={"' + obj_name + '":{"fields":["id","name"],"cond":{"in":{"name":[' + parse.quote(
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
                                    # order_data.append(temporary_cond)
                                    order_data[temporary_cond[key_name]] = temporary_cond

                                    cond['sign'] = '有值'


                            if 'sign' not in cond and cond[data_name] != None:

                                cond[data_name] = None
                                # order_data.append(cond)
                                order_data[cond[key_name]] = cond
                else:

                    for cond in data:

                        cond[data_name] = None
                        # order_data.append(cond)
                        order_data[cond[key_name]] = cond

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

                get_url = public_url + '/api/v1.0/one/dsl/query?dsl={"' + obj_name + '":{"fields":["id","' + query_code + '"],"cond":{"in":{"'+ query_code +'":[' + parse.quote(record) + ']}},"limit":500}}'

                record_id = Method(get_url).get_id()

                cond_id = get_date(get_url, record_id)

                if cond_id:

                    for cond in data:

                        if data_name in cond and 'sign' not in cond and cond[data_name] != None:

                            for info in cond_id:
                                if cond[query_name] == info[query_code]:
                                    cond[data_name] = info['id']
                                    temporary_cond = copy.deepcopy(cond)
                                    # order_data.append(temporary_cond)
                                    order_data[temporary_cond[key_name]] = temporary_cond
                                    cond['sign'] = '有值'
                                    break


                            if 'sign' not in cond and cond[data_name] != None:
                                cond[data_name] = None
                                # order_data.append(cond)
                                order_data[cond[key_name]] = cond
                else:
                    for cond in data:
                        cond[data_name] = None
                        # order_data.append(cond)
                        order_data[cond[key_name]] = cond

    return order_data

def get_time(start, end, num):

    num1 = (time.mktime(time.strptime(end, "%Y-%m-%d %H:%M:%S")) - time.mktime(
        time.strptime(start, "%Y-%m-%d %H:%M:%S"))) / num

    lis_time = []
    lis_time.append(start)
    for i in range(1, num):

        start_time = time.mktime(time.strptime(start, "%Y-%m-%d %H:%M:%S"))

        tim = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time + num1 * i))

        lis_time.append(tim)
    lis_time.append(end)

    return lis_time