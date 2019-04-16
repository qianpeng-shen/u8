# encoding=utf-8
import os
import json
import logging
import time
import http.client

from urllib import request

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
    log_path = os.path.dirname(os.getcwd()) + '/All_synchronization/Logs/'

    log_name = log_path + rq + '.log'
    logfile = log_name
    fh = logging.FileHandler(logfile, mode='w', encoding='utf-8')
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger

#执行查询插入操作
def post_meiqia(url,payload=None):
    textmod=payload
    header_dict = {
        'x-token': "Ae2CASx4I1wAAEFRQUNRcXdlWkFZQkFBQUFMYVVETFVaVFV4VXZxZ0VBQVFBQ1Fxd2VYUkVCQUFBQTM1eDc2WkhsTEJVWXBRQUEnBOEyGp4JBHD9LHCDLrUud752j_Q9WkYdGIEipr_3MOdbPM6hl4OBLSPt6jxoPT-iACZrP83BNVs_w9WOcz_c",
        'content-type': "application/json",
        'cache-control': "no-cache",
        'postman-token': "529a9a27-2e62-0d64-aea9-c938d33ec5fd"
        }
    url = "https://crm.meiqia.com" + url

    if textmod:
        try:
            # json串数据使用
            textmod = json.dumps(textmod).encode(encoding='utf-8')
            req = request.Request(url=url, data=textmod, headers=header_dict)
            res = request.urlopen(req)
            res = res.read().decode(encoding='utf-8')
            res_data = json.loads(res)

            print(res_data)

            # if res_data['code'] != 0:
            #     res_payload = payload
            #     res_url = url
            #     post_meiqia(res_payload, res_url)

        except Exception as Error:
            loger().error(Error)
    else:
        try:
            req = request.Request(url = url,headers = header_dict)
            res = request.urlopen(req)
            # print(res)
            res = res.read().decode(encoding = 'utf-8')
            return json.loads(res)['body']['objects']
        except Exception as Error:
            loger().error(Error)

#更改数据
def put_meiqia(payload, url):
    try:
        conn = http.client.HTTPSConnection("crm.meiqia.com")#连接指定的服务器
        payload = json.dumps(payload)
        headers = {
            'x-token': "Ae2CASx4I1wAAEFRQUNRcXdlWkFZQkFBQUFMYVVETFVaVFV4VXZxZ0VBQVFBQ1Fxd2VYUkVCQUFBQTM1eDc2WkhsTEJVWXBRQUEnBOEyGp4JBHD9LHCDLrUud752j_Q9WkYdGIEipr_3MOdbPM6hl4OBLSPt6jxoPT-iACZrP83BNVs_w9WOcz_c",
            'content-type': "application/json",
            'cache-control': "no-cache",
            'postman-token': "529a9a27-2e62-0d64-aea9-c938d33ec5fd"
        }

        conn.request("PUT", url, payload, headers)#使用指定的方法和url向服务器发送请求

        res = conn.getresponse()#返回一个 HTTPResponse 实例
        data = res.read().decode("utf-8")#读取内容

        data=json.loads(data)
        print(data)

        conn.close()
    except Exception as Error:
        loger().error(Error)