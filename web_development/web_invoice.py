# -*- coding:utf-8 -*-

try:
    import xml.etree.cElementTree as et
except ImportError:
    import xml.etree.ElementTree as et

from web_interface import Web_interface
from public_method import Method,analy_data,loger,cond_data

invoice = []


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
                invoice.append(dict_head)

            except Exception as error:

                loger().info("获取出库单解析数据时报错，报错信息：%s" %error)



#主程序
def main(data):

    web_order = Web_interface(data).sales_shipment()

    if not web_order:
        i = 1
        while i <= 3:

            web_order = Web_interface(data).sales_shipment()
            if web_order:

                analysis_person(web_order)
                break
            i += 1
    else:
        analysis_person(web_order)

    info_list = [['OrderInfo','sales_order']]
    invoice_data = invoice

    for i in info_list:
        invoice_data = cond_data(invoice_data,i)

    for order in analy_data(invoice_data):
        order_url = "https://crm.meiqia.com/api/v1.0/one/OrderInfo/"
        Method(order_url,{'objects':order}).post_data()





if __name__ == '__main__':
    # data = "where year(ddate)='2016' and month(ddate)='1' and breturnflag='否'"
    # main(data)
    strwhere = ["where year(ddate)='2015' and month(ddate)='1'", "where year(ddate)='2015' and month(ddate)='2'", "where year(ddate)='2015' and month(ddate)='3'", "where year(ddate)='2015' and month(ddate)='4'", "where year(ddate)='2015' and month(ddate)='5'", "where year(ddate)='2015' and month(ddate)='6'", "where year(ddate)='2015' and month(ddate)='7'", "where year(ddate)='2015' and month(ddate)='8'", "where year(ddate)='2015' and month(ddate)='9'", "where year(ddate)='2015' and month(ddate)='10'", "where year(ddate)='2015' and month(ddate)='11'", "where year(ddate)='2015' and month(ddate)='12'", "where year(ddate)='2016' and month(ddate)='1'", "where year(ddate)='2016' and month(ddate)='2'", "where year(ddate)='2016' and month(ddate)='3'", "where year(ddate)='2016' and month(ddate)='4'", "where year(ddate)='2016' and month(ddate)='5'", "where year(ddate)='2016' and month(ddate)='6'", "where year(ddate)='2016' and month(ddate)='7'", "where year(ddate)='2016' and month(ddate)='8'", "where year(ddate)='2016' and month(ddate)='9'", "where year(ddate)='2016' and month(ddate)='10'", "where year(ddate)='2016' and month(ddate)='11'", "where year(ddate)='2016' and month(ddate)='12'", "where year(ddate)='2017' and month(ddate)='1'", "where year(ddate)='2017' and month(ddate)='2'", "where year(ddate)='2017' and month(ddate)='3'", "where year(ddate)='2017' and month(ddate)='4'", "where year(ddate)='2017' and month(ddate)='5'", "where year(ddate)='2017' and month(ddate)='6'", "where year(ddate)='2017' and month(ddate)='7'", "where year(ddate)='2017' and month(ddate)='8'", "where year(ddate)='2017' and month(ddate)='9'", "where year(ddate)='2017' and month(ddate)='10'", "where year(ddate)='2017' and month(ddate)='11'", "where year(ddate)='2017' and month(ddate)='12'", "where year(ddate)='2018' and month(ddate)='1'", "where year(ddate)='2018' and month(ddate)='2'", "where year(ddate)='2018' and month(ddate)='3'", "where year(ddate)='2018' and month(ddate)='4'", "where year(ddate)='2018' and month(ddate)='5'", "where year(ddate)='2018' and month(ddate)='6'", "where year(ddate)='2018' and month(ddate)='7'", "where year(ddate)='2018' and month(ddate)='8'", "where year(ddate)='2018' and month(ddate)='9'", "where year(ddate)='2018' and month(ddate)='10'", "where year(ddate)='2018' and month(ddate)='11'", "where year(ddate)='2018' and month(ddate)='12'", "where year(ddate)='2019' and month(ddate)='1'", "where year(ddate)='2019' and month(ddate)='2'", "where year(ddate)='2019' and month(ddate)='3'", "where year(ddate)='2019' and month(ddate)='4'", "where year(ddate)='2019' and month(ddate)='5'", "where year(ddate)='2019' and month(ddate)='6'", "where year(ddate)='2019' and month(ddate)='7'", "where year(ddate)='2019' and month(ddate)='8'", "where year(ddate)='2019' and month(ddate)='9'", "where year(ddate)='2019' and month(ddate)='10'", "where year(ddate)='2019' and month(ddate)='11'", "where year(ddate)='2019' and month(ddate)='12'"]
    for data in strwhere:

        data = data + " and breturnflag='否'"
        main(data)