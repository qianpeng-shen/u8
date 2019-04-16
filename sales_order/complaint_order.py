# -*- coding:utf-8 -*-
from common_method import cond_data

#解析投诉工单
def analysis_complaint(data):
    complaint_list = []

    for complaint in range(1,data.nrows):
        complaint_dict = {}
        complaint_dict['Status'] = data.cell(complaint,1).value
        complaint_dict['UserID_ZDR'] = data.cell(complaint,7).value
        complaint_dict['AdgroupID'] = data.cell(complaint,8).value
        complaint_dict['UserID_KF'] = data.cell(complaint,10).value
        if data.cell(complaint,11).value:
            if data.cell(complaint,11).value == '网页表单':
                complaint_dict['CreateOrderChannel'] = '线上'
            else:
                complaint_dict['CreateOrderChannel'] = '电话'
        complaint_dict['DetailContentMore'] = data.cell(complaint,12).value
        if data.cell(complaint,13).value:
            complaint_dict['CallerNumber_Hand'] = '+86 ' + data.cell(complaint,13).value
        complaint_dict['UserName'] = data.cell(complaint,20).value
        complaint_dict['ProvinceID'] = data.cell(complaint,22).value
        complaint_dict['MunicipalityID'] = data.cell(complaint,23).value
        complaint_dict['PrefectureID'] = data.cell(complaint,24).value
        complaint_dict['Address_Detail'] = data.cell(complaint,34).value
        # complaint_dict['ComplaintContent'] = data.cell(complaint,38).value
        complaint_dict['Remarks'] = '系统流水号:' + str(data.cell(complaint,1).value) + '\n工单来源:' + data.cell(complaint,36).value + '\n产品名称:' + data.cell(complaint,37).value + '\n详细地址:' + data.cell(complaint,39).value + '\n通话详情内容:' + data.cell(complaint,41).value
        complaint_list.append(complaint_dict)
        print(complaint_dict)
        break
    info_list = [['Province', 'ProvinceID'], ['Municipality', 'MunicipalityID'], ['Prefecture', 'PrefectureID'],['User', 'UserID_ZDR', 'UserID_ZDR', 'PersonCode'],['User','UserID_KF'],['Adgroup','AdgroupID']]

    for i in info_list:
        complaint_list = cond_data(complaint_list, i)
    return complaint_list


