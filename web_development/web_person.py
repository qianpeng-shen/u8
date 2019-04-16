# -*- coding:utf-8 -*-

try:
    import xml.etree.cElementTree as et
except ImportError:
    import xml.etree.ElementTree as et

from web_interface import Web_interface
from public_method import Method,analy_data,loger

person = {}

def analysis_person(data):

    data = et.fromstring(data)

    if data:
        for i in data:
            try:
                if not i.find('dLeaveDate').text :#停用时间无值时，执行下面程序
                    dict_p = {}
                    dict_p['PersonnelNumber'] = i.find('cPsn_Num').text #人员编码
                    dict_p['name'] = i.find('cPsn_Name').text #人员名称
                    dict_p['Employment_status'] = i.find('vsimpleName').text #雇佣状态
                    dict_p['DepartmentCode'] = i.find('cDept_num').text #部门编码
                    dict_p['DepartmentName'] = i.find('cDepName').text #部门名称
                    dict_p['web_create_time'] = i.find('dEnterUnitDate').text #建档日期
                    dict_p['web_modify_time'] = i.find('dLastDate').text #修改日期

                    person[i.find('cPsn_Name').text] = dict_p
            except Exception as error:
                loger().info(error)

#主程序
def main():

    web_person = Web_interface().person_info()

    if not web_person:
        i = 1
        while i <= 3:

            web_data = Web_interface().person_info()
            if web_data:

                analysis_person(web_person)
                break
            i += 1
    else:
        analysis_person(web_person)

    list_person = list(person.values())
    analy_sn = analy_data(list_person)
    for i in analy_sn:

        url = "https://crm.meiqia.com/api/v1.0/one/Salesman/"
        Method(url,{'objects':i}).post_data()


if __name__ == '__main__':
    main()