# -*- coding:utf-8 -*-
from common_method import cond_data
#解析拆机工单
def analysis_dismantling(data):

    dismantling_list = []
    for dismantling in range(1,data.nrows):

        dismantling_dict = {}
        service_dict = {}
        visit_dict = {}
        dismantling_dict['Status'] = data.cell(dismantling,1).value
        dismantling_dict['UserID_ZDR'] = data.cell(dismantling,7).value
        dismantling_dict['AdgroupID'] = data.cell(dismantling,8).value
        dismantling_dict['UserID_KF'] = data.cell(dismantling,10).value
        if data.cell(dismantling,11).value:
            if data.cell(dismantling,11).value == '网页表单':
                dismantling_dict['CreateOrderChannel'] = '线上'
            else:
                dismantling_dict['CreateOrderChannel'] = '电话'
        dismantling_dict['DetailContentMore'] = data.cell(dismantling,12).value
        # if data.cell(dismantling,13).value:
            # dismantling_dict['CallerNumber_Hand'] = '+86 ' + data.cell(dismantling,13).value
        dismantling_dict['UserName'] = data.cell(dismantling,20).value
        dismantling_dict['ProvinceID'] = data.cell(dismantling,22).value
        dismantling_dict['MunicipalityID'] = data.cell(dismantling,23).value
        dismantling_dict['PrefectureID'] = data.cell(dismantling,24).value
        dismantling_dict['Address_Detail'] = data.cell(dismantling,34).value
        dismantling_dict['SN_GDXX'] = data.cell(dismantling,38).value
        dismantling_dict['AppointmentTime'] = (data.cell(dismantling,40).value).replace('/','-') + "T00:00:00Z"
        dismantling_dict['Remarks'] = '系统流水号:' + str(data.cell(dismantling,1).value) + '\n通话号码:' + data.cell(dismantling,16).value + '\n工单来源:' + data.cell(dismantling,36).value + '\n产品名称:' + data.cell(dismantling,37).value + '\n详细地址:' + data.cell(dismantling,39).value
        if data.cell(dismantling,41).value:
            service_dict['ServiceProvidersNumber'] = data.cell(dismantling,41).value
        if data.cell(dismantling,42).value:
            service_dict['ActivityContent'] = data.cell(dismantling,42).value
        if data.cell(dismantling,43).value:
            visit_dict['Situation'] = data.cell(dismantling,43).value
        if data.cell(dismantling,44).value:
            visit_dict['Reason'] = data.cell(dismantling,44).value
        if service_dict:
            dismantling_dict['service'] = service_dict
        if visit_dict:
            dismantling_dict['visit'] = visit_dict
        dismantling_list.append(dismantling_dict)
        print(dismantling_list)
        break
    info_list = [['Province', 'ProvinceID'], ['Municipality', 'MunicipalityID'], ['Prefecture', 'PrefectureID'],['User', 'UserID_ZDR', 'UserID_ZDR', 'PersonCode'],['User','UserID_KF'],['Adgroup','AdgroupID']]

    for i in info_list:
        dismantling_list = cond_data(dismantling_list, i)
    print(dismantling_list)
    return dismantling_list

