# -*- coding:utf-8 -*-
from common_method import cond_data
#咨询工单
def analysis_consultative(data):
    new_list = []
    for r in range(1,data.nrows):
        new_dict = {}

        new_dict['Status'] = data.cell(r,1).value
        new_dict['UserID_ZDR'] = data.cell(r,7).value
        new_dict['AdgroupID'] = data.cell(r,8).value
        new_dict['UserID_KF'] = data.cell(r,10).value
        if data.cell(r,11).value:
            if data.cell(r,11).value == '网页表单':
                new_dict['CreateOrderChannel'] = '线上'
            else:
                new_dict['CreateOrderChannel'] = '电话'
        new_dict['DetailedDescription'] = data.cell(r,12).value
        new_dict['CallerNumber_Hand'] =  "+86 " + data.cell(r,13).value
        new_dict['UserName'] = data.cell(r,20).value
        new_dict['ProvinceID'] = data.cell(r,22).value
        new_dict['MunicipalityID'] = data.cell(r,23).value
        new_dict['PrefectureID'] = data.cell(r,24).value
        new_dict['Address_Detail'] = data.cell(r,34).value
        new_dict['ConsultationType'] = '售前'
        if data.cell(r,38).value:
            new_dict['PreSaleConsultationContent'] = data.cell(r,38).value
        new_dict['Remarks'] = '系统流水号:' + str(data.cell(r,0).value) + '\n通话号码:' + data.cell(r,16).value + '\n工单来源:' + data.cell(r,36).value + '\n产品名称:' + data.cell(r,37).value + '\n各产品现象:' + data.cell(r,39).value + '\n通话详细内容:' + data.cell(r,40).value

        new_list.append(new_dict)

    info_list = [['Province', 'ProvinceID'], ['Municipality', 'MunicipalityID'], ['Prefecture', 'PrefectureID'],['User', 'UserID_ZDR', 'UserID_ZDR', 'PersonCode'],['User','UserID_KF'],['Adgroup','AdgroupID']]

    for i in info_list:
        new_list = cond_data(new_list, i)

    return new_list
#PreSaleConsultationContent    ConsultationType

