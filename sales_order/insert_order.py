# -*- coding:utf-8 -*-
from common_method import cond_data

#解析安装工单
def analysis_insert(data):

    insert_list = []
    for insert in (1,data.nrows):
        primary_dict = {}
        service_dict = {}
        primary_dict['Status'] = data.cell(insert,1).value
        primary_dict['UserID_ZDR'] = data.cell(insert,7).value
        primary_dict['AdgroupID'] = data.cell(insert,8).value
        primary_dict['UserID_KF'] = data.cell(insert,10).value
        if data.cell(insert,11).value:
            if data.cell(insert,11).value == '网页表单':
                primary_dict['CreateOrderChannel'] = '线上'
            else:
                primary_dict['CreateOrderChannel'] = '电话'
        primary_dict['DetailContentMore'] = data.cell(insert,12).value
        primary_dict['CallerNumber_Hand'] = '+86 ' + data.cell(insert,13).value
        primary_dict['UserName'] = data.cell(insert,20).value
        primary_dict['ProvinceID'] = data.cell(insert,22).value
        primary_dict['MunicipalityID'] = data.cell(insert,23).value
        primary_dict['PrefectureID'] = data.cell(insert,24).value
        primary_dict['PurchaseChannelID'] = data.cell(insert,37).value
        primary_dict['SN_GDXX'] = data.cell(insert,39).value
        primary_dict['Address_Detail'] = data.cell(insert,40).value

        primary_dict['AppointmentTime'] = (data.cell(insert,41).value).replace('/','-') + "T00:00:00Z"
        primary_dict['Remarks'] = '系统流水号：' + str(data.cell(insert,0).value) + '\n通话号码:' + data.cell(insert,16).value + '\n工单来源:' + data.cell(insert,36).value + '\n产品名称:' + data.cell(insert,38).value
        if data.cell(insert,42).value:
            service_dict['RelatedServiceProvider'] = data.cell(insert,42).value
        if data.cell(insert,43).value:
            service_dict['ServiceProvidersNumber'] = data.cell(insert,43).value
        if service_dict:
            primary_dict['service'] = service_dict
        insert_list.append(primary_dict)
        print(primary_dict)
        break
    info_list = [['Province', 'ProvinceID'], ['Municipality', 'MunicipalityID'], ['Prefecture', 'PrefectureID'],['User', 'UserID_ZDR', 'UserID_ZDR', 'PersonCode'],['User','UserID_KF'],['Adgroup','AdgroupID']]

    for i in info_list:
        insert_list = cond_data(insert_list, i)

    return insert_list


