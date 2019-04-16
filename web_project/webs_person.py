# -*- coding:utf-8 -*-

try:
    import xml.etree.cElementTree as et
except ImportError:
    import xml.etree.ElementTree as et

from webs_interfaces import Web_interface
from public_methods import get_record,loger

import datetime

person = {}

def analysis_person(data):

    data = et.fromstring(data)

    if data:
        for i in data:
            try:
                dict_p = {}
                dict_p['PersonnelNumber'] = i.find('cPsn_Num').text #人员编码
                dict_p['name'] = i.find('cPsn_Name').text #人员名称
                if i.find('vsimpleName') != None and i.find('vsimpleName').text:
                    if i.find('vsimpleName').text in ['离职','离退']:
                        dict_p['Employment_status'] = i.find('vsimpleName').text  # 雇佣状态
                        dict_p['end_time'] = '离职'
                    else:
                        dict_p['Employment_status'] = i.find('vsimpleName').text
                dict_p['DepartmentCode'] = i.find('cDept_num').text #部门编码
                dict_p['DepartmentName'] = i.find('cDepName').text #部门名称
                dict_p['web_create_time'] = i.find('dEnterUnitDate').text #建档日期

                # if i.find('dLeaveDate').text:
                #     dict_p['end_time'] = i.find('dLeaveDate').text #停用时间
                dict_p['web_modify_time'] = i.find('dLastDate').text #修改时间

                person[i.find('cPsn_Num').text] = dict_p

            except Exception as error:
                loger().info(error)

#主程序
def main():

    time_begin = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
    time_end = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%Y-%m-%d") + ' 23:59:59'
    strwhere = "where dLastDate>='%s' and dLastDate<='%s'" % (time_begin, time_end)
    strwhere = "where dLastDate>='2019-02-22 00:00:00' and dLastDate<='2019-02-22 23:00:00'"
    web_person = Web_interface(strwhere).person_info()

    if not web_person:
        i = 1
        while i <= 3:

            web_data = Web_interface(strwhere).person_info()
            if web_data:

                analysis_person(web_person)
                break
            i += 1
    else:
        analysis_person(web_person)
    # print(person)
    if person:

        get_record(person,'Salesman','PersonnelNumber')


if __name__ == '__main__':
    main()