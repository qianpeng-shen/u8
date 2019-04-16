# -*- coding:utf-8 -*-
import re
try:
    import xml.etree.cElementTree as et
except ImportError:
    import xml.etree.ElementTree as et

from webs_interfaces import Web_interface
from public_methods import get_record,loger
import datetime

customer = {}

def mobile(data):
    phone = data
    if phone.startswith('1'):
        phone_re = '^((13[0-9])|(14[5,7])|(15[0-3,5-9])|(17[0,3,5-8])|(18[0-9])|166|198|199|(147))\\d{8}$'
        if re.search(phone_re,phone):
            return '+86 ' + phone
    else:
        mobile_re = '0\d{2,3}-\d{7,8}'
        if '-' in phone:
            if re.search(mobile_re,phone):
                return '+86 ' + phone
        else:
            if re.search(mobile_re,phone):
                return '+86 ' + phone


def analysis_customer(data):

    data = et.fromstring(data)

    if data:
        for i in data:
            try:
                dict_c = {}
                dict_c['name'] = i.find('cCusName').text #客户名称
                dict_c['channel_code'] = i.find('cCusCode').text #客户编码
                dict_c['ChannelContact'] = i.find('cContactName').text #联系人
                dict_c['ChannelAddress'] = i.find('cCusAddress').text #联系地址

                if i.find('cCusPhone').text:
                    cusphone = mobile(i.find('cCusPhone').text)
                    if cusphone:
                        dict_c['ChannelPhone'] = cusphone #联系电话
                    else:
                        dict_c['Remarks'] = '联系电话:' + i.find('cCusPhone').text
                if i.find('dEnterUnitDate'):
                    dict_c['dCusCreateDatetime'] = i.find('dCusCreateDatetime').text #建档日期

                dict_c['web_modify_time'] = i.find('dModifyDate').text #修改日期

                customer[i.find('cCusCode').text] = dict_c

            except Exception as error :
                loger().info(error)

#主程序
def main():

    time_begin = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
    time_end = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%Y-%m-%d") + ' 23:59:59'
    strwhere = "where dModifyDate>='%s' and dModifyDate<='%s'"%(time_begin,time_end)
    strwhere = "where dModifyDate>='2019-02-22 00:00:00' and dModifyDate<='2019-02-22 23:00:00'"

    web_customer = Web_interface(strwhere).customer_info()

    if not web_customer:
        i = 1
        while i <= 3:

            web_data = Web_interface(strwhere).customer_info()
            if web_data:
                analysis_customer(web_customer)
                break
            i += 1
    else:
        analysis_customer(web_customer)
    print(customer)
    if customer:

        get_record(customer,'Channel','channel_code')


if __name__ == '__main__':
    main()