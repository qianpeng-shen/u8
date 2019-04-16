# -*- coding:utf-8 -*-
import re
try:
    import xml.etree.cElementTree as et
except ImportError:
    import xml.etree.ElementTree as et

from web_interface import Web_interface
from public_method import Method,analy_data,loger,cond_data

receipt = []

def analysis_person(data):

    data = et.fromstring(data)

    if data:
        for i in data:
            try:

                dict_h = {}
                dict_h['number_delivery'] = i.find('ccode').text #出库单号
                dict_h['sales_order'] = i.find('csocode').text #销售订单号
                dict_h['receipt_id'] = i.find('id').text  # 销售出库单ID
                dict_h['outbound_date'] = i.find('ddate').text #出库日期
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

                receipt.append(dict_h)

            except Exception as error:
                loger().info("获取销售发货单解析是报错，报错信息是：%s" %error)



#主程序
def main(data):

    global receipt
    web_order = Web_interface(data).sales_outlet()

    if not web_order:
        i = 1
        while i <= 3:

            web_order = Web_interface(data).sales_outlet()
            if web_order:

                analysis_person(web_order)
                break
            i += 1
    else:
        analysis_person(web_order)

    info_list = [['OrderInfo','sales_order']]
    receipt_data = receipt

    for info in info_list:

        receipt_data = cond_data(receipt_data,info)

    for order in analy_data(receipt_data):
        order_url = "https://crm.meiqia.com/api/v1.0/one/SalesReceipt/"
        Method(order_url,{'objects':order}).post_data()





if __name__ == '__main__':
    strwhere = ["where year(ddate)='2015' and month(ddate)='1'", "where year(ddate)='2015' and month(ddate)='2'", "where year(ddate)='2015' and month(ddate)='3'", "where year(ddate)='2015' and month(ddate)='4'", "where year(ddate)='2015' and month(ddate)='5'", "where year(ddate)='2015' and month(ddate)='6'", "where year(ddate)='2015' and month(ddate)='7'", "where year(ddate)='2015' and month(ddate)='8'", "where year(ddate)='2015' and month(ddate)='9'", "where year(ddate)='2015' and month(ddate)='10'", "where year(ddate)='2015' and month(ddate)='11'", "where year(ddate)='2015' and month(ddate)='12'", "where year(ddate)='2016' and month(ddate)='1'", "where year(ddate)='2016' and month(ddate)='2'", "where year(ddate)='2016' and month(ddate)='3'", "where year(ddate)='2016' and month(ddate)='4'", "where year(ddate)='2016' and month(ddate)='5'", "where year(ddate)='2016' and month(ddate)='6'", "where year(ddate)='2016' and month(ddate)='7'", "where year(ddate)='2016' and month(ddate)='8'", "where year(ddate)='2016' and month(ddate)='9'", "where year(ddate)='2016' and month(ddate)='10'", "where year(ddate)='2016' and month(ddate)='11'", "where year(ddate)='2016' and month(ddate)='12'", "where year(ddate)='2017' and month(ddate)='1'", "where year(ddate)='2017' and month(ddate)='2'", "where year(ddate)='2017' and month(ddate)='3'", "where year(ddate)='2017' and month(ddate)='4'", "where year(ddate)='2017' and month(ddate)='5'", "where year(ddate)='2017' and month(ddate)='6'", "where year(ddate)='2017' and month(ddate)='7'", "where year(ddate)='2017' and month(ddate)='8'", "where year(ddate)='2017' and month(ddate)='9'", "where year(ddate)='2017' and month(ddate)='10'", "where year(ddate)='2017' and month(ddate)='11'", "where year(ddate)='2017' and month(ddate)='12'", "where year(ddate)='2018' and month(ddate)='1'", "where year(ddate)='2018' and month(ddate)='2'", "where year(ddate)='2018' and month(ddate)='3'", "where year(ddate)='2018' and month(ddate)='4'", "where year(ddate)='2018' and month(ddate)='5'", "where year(ddate)='2018' and month(ddate)='6'", "where year(ddate)='2018' and month(ddate)='7'", "where year(ddate)='2018' and month(ddate)='8'", "where year(ddate)='2018' and month(ddate)='9'", "where year(ddate)='2018' and month(ddate)='10'", "where year(ddate)='2018' and month(ddate)='11'", "where year(ddate)='2018' and month(ddate)='12'", "where year(ddate)='2019' and month(ddate)='1'", "where year(ddate)='2019' and month(ddate)='2'", "where year(ddate)='2019' and month(ddate)='3'", "where year(ddate)='2019' and month(ddate)='4'", "where year(ddate)='2019' and month(ddate)='5'", "where year(ddate)='2019' and month(ddate)='6'", "where year(ddate)='2019' and month(ddate)='7'", "where year(ddate)='2019' and month(ddate)='8'", "where year(ddate)='2019' and month(ddate)='9'", "where year(ddate)='2019' and month(ddate)='10'", "where year(ddate)='2019' and month(ddate)='11'", "where year(ddate)='2019' and month(ddate)='12'"]
    for data in strwhere:
    # data = "where year(ddate)='2018' and month(ddate)='1'"
        main(data)