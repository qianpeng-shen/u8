# -*- coding:utf-8 -*-
try:
    import xml.etree.cElementTree as et
except ImportError:
    import xml.etree.ElementTree as et

from webs_interfaces import Web_interface
from public_methods import loger,cond_data,get_record,get_time

import math
import datetime

invoice = {}


def analysis_person(data):

    data = et.fromstring(data)

    if data:
        for i in data:

            try:

                dict_head = {}

                dict_head['ship_date'] = i.find('ddate').text + "T" + "00:00:00Z"  # 发货日期
                dict_head['shipment_number'] = i.find('cdlcode').text  # 发货单号
                dict_head['invoice_id'] = i.find('dlid').text  # 销售发货单ID
                dict_head['sales_order'] = i.find('csocode').text  # 销售订单号
                dict_head['tracking_number'] = i.find('cebexpresscode').text  # 物流单号
                if i.find('dcreatesystime') != None:
                    create_time = i.find('dcreatesystime').text
                    if create_time and ' ' in create_time and '.' in create_time:
                        create_time = create_time.split(' ')
                        create_time = create_time[0] + 'T' + create_time[1]
                        create_time = create_time.split('.')
                    dict_head['create_date'] = create_time[0] + 'Z'  # 建档时间
                if i.find('dbgdatetime') != None:
                    update_date = i.find('dbgdatetime').text
                    if update_date and '.' in update_date and 'T' in update_date:
                        update_time = update_date.split('.')
                        dict_head['update_date'] = update_time[0] + update_time[1] + 'Z'  # 修改时间
                invoice[i.find('dlid').text] = dict_head

            except Exception as error:

                loger().info("获取发货单解析数据时报错，报错信息：%s" %error)



#主程序
def main(cond):

    web_order = Web_interface(cond).sales_shipment()

    if not web_order:
        i = 1
        while i <= 3:

            web_order = Web_interface(cond).sales_shipment()
            if web_order:

                analysis_person(web_order)
                break
            i += 1
    else:
        analysis_person(web_order)
    print(invoice)
    if invoice:
        info_list = [['OrderInfo','sales_order']]
        invoice_data = invoice

        for i in info_list:
            invoice_data = cond_data(invoice_data,i,'invoice_id')

        get_record(invoice_data,"SalesInvoice","invoice_id")

def invoice_main():

    time_begin = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
    time_end = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%Y-%m-%d") + ' 23:59:59'
    strwhere = "where dbgdatetime>='%s' and dbgdatetime<='%s'" % (time_begin, time_end)
    strwhere = "where dbgdatetime>='2019-02-25 00:00:00' and dbgdatetime<='2019-02-25 23:00:00'"
    order_count = Web_interface(strwhere).web_shipmentcount()
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
    order_count = Web_interface(strwhere).web_shipmentcount()
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