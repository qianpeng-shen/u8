# # -*- coding:utf-8 -*-
import xlrd
import json
import os
import logging
import time
from urllib import request

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

#打开数据所在的工作簿，以及选择存有数据的工作表
book = xlrd.open_workbook("1-201601-20161130.xlsx")
sheet = book.sheet_by_name("咨询工单")

# 创建一个for循环迭代读取xls文件每行数据的, 从第二行开始是要跳过标题行
def analysis_sales(sheet):
    for r in range(1, sheet.nrows):
        # new_data ={}
        # new_data['number_id'] = sheet.cell_value(r,1)
        # new_data['status'] = sheet.cell(r,2).value
        # new_data['name'] = sheet.cell(r,3).value
        # new_data['create_by'] = sheet.cell(r,4).value
        # new_data['create_end'] = sheet.cell(r,5).value
        # new_data['create_time'] = sheet.cell(r,6).value
        # new_data['create_name'] = sheet.cell(r,7).value
        # new_data['create_num'] = sheet.cell(r,8).value
        # new_data['group_order'] = sheet.cell(r,8).value
        # new_data['order_data'] = sheet.cell(r,9).value
        # new_data['maker'] = sheet.cell(r,10).value
        # new_data['channel'] = sheet.cell(r,11).value
        # new_data['description'] = sheet.cell(r,12).value
        if sheet.cell(r,20).value:
            print(sheet.cell(r,20).value)

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

            logger.info('执行新增时报错，报错为:%s'%error)
def main():
    analysis_sales(sheet)

if __name__ == "__main__":
    main()
