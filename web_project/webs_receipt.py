# -*- coding:utf-8 -*-
try:
    import xml.etree.cElementTree as et
except ImportError:
    import xml.etree.ElementTree as et

from webs_interfaces import Web_interface
from public_methods import loger,cond_data,get_record,get_time

import datetime
import math

receipt = {}

def analysis_person(data):

    data = et.fromstring(data)

    if data:
        for i in data:
            try:

                dict_h = {}
                dict_h['number_delivery'] = i.find('ccode').text #出库单号
                dict_h['sales_order'] = i.find('csocode').text #销售订单号
                dict_h['receipt_id'] = i.find('id').text  # 销售出库单ID

                dict_h['outbound_date'] = i.find('ddate').text + 'Z'#出库日期
                if i.find('cebexpresscode') != None:
                    dict_h['shipment_number'] = i.find('cebexpresscode').text #物流单号
                if i.find('dbgdatetime') != None:
                    update_date = i.find('dbgdatetime').text
                    if update_date  and '.' in update_date and 'T' in update_date:
                        update_time = update_date.split('.')
                        dict_h['update_date'] = update_time[0] + update_time[1] + 'Z' #修改时间
                if i.find('dnmaketime') != None:
                    maketime = i.find('dnmaketime').text
                    if maketime and ' ' in maketime and '.' in maketime:
                        maketime = maketime.split(' ')
                        maketime = maketime[0] + 'T' + maketime[1]
                        maketime = maketime.split('.')

                    dict_h['create_date'] = maketime[0] + 'Z' #建档时间
                receipt[i.find('id').text] = dict_h


            except Exception as error:
                loger().info("获取销售发货单解析是报错，报错信息是：%s" %error)



#主程序
def main(cond):

    web_order = Web_interface(cond).sales_outlet()

    if not web_order:
        i = 1
        while i <= 3:

            web_order = Web_interface(cond).sales_outlet()
            if web_order:

                analysis_person(web_order)
                break
            i += 1
    else:
        analysis_person(web_order)

    if receipt:

        info_list = [['OrderInfo','sales_order']]
        receipt_data = receipt

        for info in info_list:

            receipt_data = cond_data(receipt_data,info,'receipt_id')


        get_record(receipt_data,"SalesReceipt","receipt_id")

def receipt_main():

    time_begin = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
    time_end = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%Y-%m-%d") + ' 23:59:59'
    strwhere = "where dbgdatetime>='%s' and dbgdatetime<='%s'" % (time_begin, time_end)
    strwhere = "where dbgdatetime>='2019-02-25 00:00:00' and dbgdatetime<='2019-02-25 23:00:00'"
    order_count = Web_interface(strwhere).web_outletcount()
    if order_count:
        condition = []
        if order_count <5000:
            condition.append(strwhere)
        else:
            number = math.ceil(order_count/5000)
            lis_time = get_time(time_begin,time_end,number)
            for i in range(number):
                str_time = "where dbgdatetime>='%s' and dbgdatetime<='%s'" %(lis_time[i],lis_time[i+1])
                condition.append(str_time)

        for cond in condition:
            main(cond)

if __name__ == '__main__':

    time_begin = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
    time_end = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%Y-%m-%d") + ' 23:59:59'
    strwhere = "where dbgdatetime>='%s' and dbgdatetime<='%s'" % (time_begin, time_end)
    strwhere = "where dbgdatetime>='2019-02-25 00:00:00' and dbgdatetime<='2019-02-25 23:00:00'"
    order_count = Web_interface(strwhere).web_outletcount()
    if order_count:
        condition = []
        if order_count <5000:
            condition.append(strwhere)
        else:
            number = math.ceil(order_count/5000)
            lis_time = get_time(time_begin,time_end,number)
            for i in range(number):
                str_time = "where dbgdatetime>='%s' and dbgdatetime<='%s'" %(lis_time[i],lis_time[i+1])
                condition.append(str_time)

        for cond in condition:
            main(cond)