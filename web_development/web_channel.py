# -*- coding:utf-8 -*-
import re
try:
    import xml.etree.cElementTree as et
except ImportError:
    import xml.etree.ElementTree as et

from web_interface import Web_interface
from public_method import Method,analy_data,loger

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

                dict_c['dCusCreateDatetime'] = i.find('dCusCreateDatetime').text #建档日期

                dict_c['web_modify_time'] = i.find('dModifyDate').text #修改日期
                customer[i.find('cCusCode').text] = dict_c


            except Exception as error :
                loger().info(error)

#主程序
def main():

    web_customer = Web_interface().customer_info()

    if not web_customer:
        i = 1
        while i <= 3:

            web_data = Web_interface().customer_info()
            if web_data:
                analysis_customer(web_customer)
                break
            i += 1
    else:
        analysis_customer(web_customer)
    list_customer = list(customer.values())
    analy_customer = analy_data(list_customer)

    for i in analy_customer:


        url = "https://crm.meiqia.com/api/v1.0/one/Channel/"
        Method(url,{'objects':i}).post_data()


if __name__ == '__main__':
    main()