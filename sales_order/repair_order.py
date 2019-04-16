# -*- coding:utf-8 -*-

#解析维修类维修工单数据
def analysis_repair(data):

    repair_list = []
    for repair in range(1,data.nrows):

        repair_dict = {}

        repair_dict['Status'] = data.cell(repair,1).value
        repair_dict['UserID_ZDR'] = data.cell(repair,7).value
        repair_dict['AdgoupID'] = data.cell(repair,8).value
        repair_dict['UserID_KF'] = data.cell(repair,10).value
        if data.cell(repair,11).vlaue:
            if data.cell(repair,11).value == '网页表单':
                repair_dict['CreateOrderChannel'] = '线上'
            else:
                repair_dict['CreateOrderChannel'] = '电话'
        repair_dict['DetailContentMore'] = data.cell(repair,12).value
        repair_dict['CallerNumber'] = data.cell(repair,13).value
        repair_dict['UserName'] = data.cell(repair,20).value
        repair_dict['ProvinceID'] = data.cell(repair,22).value
        repair_dict['MunicipalityID'] = data.cell(repair,23).value
        repair_dict['PrefectureID'] = data.cell(repair,24).value
        repair_dict['Address_Detail'] = data.cell(repair,34).value
        repair_dict['SN_GDXX'] = data.cell(repair,38).value
        repair_dict['AppointmentTime'] = (data.cell(repair,40).value).replace('/','-') + 'T00"00:00Z'
        repair_dict['WarrantyPeriod'] = data.cell(repair,41).value
        if data.cell(repair,43).value:
            malfunction = data.cell(repair,43).value
            if ',' in malfunction:
                repair_dict['Breakdown_PhenomenonID'] = malfunction.split(',')[1]

        repair_dict['RelatedServiceProvider'] = data.cell(repair,46).value
        repair_dict['ServiceProvidersNumber'] = data.cell(repair,48).value
        repair_dict['ActivityContent'] = data.cell(repair,49).value
        repair_dict['Reason'] = data.cell(repair,50).value
        repair_dict['MailingAddress'] = data.cell(repair,52).value
        repair_dict['ReturnToLogistics'] = data.cell(repair,53).value





