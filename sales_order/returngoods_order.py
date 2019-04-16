# -*- coding:utf-8 -*-

from common_method import cond_data

#解析退货工单

def returngoods_order(data):

    returngoods_list = []
    for returngoods in range(1,data.nrows):
        returngoods_dict = {}
        returngoods_dict['Status'] = data.cell(returngoods,1).value
        returngoods_dict['UserID_ZDR'] = data.cell(returngoods,7).value
        returngoods_dict['AdgroupID'] = data.cell(returngoods,8).value
        returngoods_dict['UserID_KF'] = data.cell(returngoods,10).value
        if data.cell(returngoods,11).value:
            if data.cell(returngoods,11).value == '网页表单':
                returngoods_dict['CreateOrderChannel'] = '线上'
            else:
                returngoods_dict['CreateOrderChannel'] = '电话'
        returngoods_dict['DetailedDescription'] = data.cell(returngoods,12).value
        if data.cell(returngoods,13).value:
            returngoods_dict['CallerNumber_Hand'] = '+86 ' + data.cell(returngoods,13).value
        returngoods_dict['UserName'] = data.cell(returngoods,20).value
        returngoods_dict['ProvinceID'] = data.cell(returngoods,22).value
        returngoods_dict['MunicipalityID'] = data.cell(returngoods,23).value
        returngoods_dict['PrefectureID'] = data.cell(returngoods,24).value
        returngoods_dict['Address_Detail'] = data.cell(returngoods,34).value
        returngoods_dict['SN_GDXX'] = data.cell(returngoods,37).value
        returngoods_dict['XSNumbers_GDXX_lookup'] = data.cell(returngoods,38).value
        returngoods_dict['PurchaseChannel_GDXX'] = data.cell(returngoods,39).value
        if data.cell(returngoods,41).value:
            reason = data.cell(returngoods,41).value
            if ',' in reason :
                if reason.split('，')[0] in ['不想要','买错了','不匹配','多买','不认同产品性能']:
                    returngoods_dict['ReturnReason'] = reason.splait('，')[0]
            else:
                if reason in ['不想要','买错了','不匹配','多买','不认同产品性能']:
                    returngoods_dict['ReturnReason'] = reason
        returngoods_dict['DetailContentMore'] = data.cell(returngoods,42).value
        if data.cell(returngoods,43).value:
            warehouse = data.cell(returngoods,43).value
            if '回' in warehouse :
                if warehouse.split('，')[0] in ['不想要','买错了','不匹配','多买','不认同产品性能']:
                    returngoods_dict['ReturnEntrepot'] = warehouse.splait('，')[1]
            else:
                if warehouse in ['慈溪仓','首钢国际仓','京东仓','菜鸟仓',]:

                    returngoods_dict['ReturnEntrepot'] = warehouse
        returngoods_dict['Logistics'] = data.cell(returngoods,44).value
        returngoods_dict['Remarks'] = '系统流水号:' + str(data.cell(returngoods,0).value)
        returngoods_list.append(returngoods_dict)

    info_list = [['Province', 'ProvinceID'], ['Municipality', 'MunicipalityID'], ['Prefecture', 'PrefectureID'],['OrderInfo','XSNumbers_GDXX_lookup'],['User', 'UserID_ZDR', 'UserID_ZDR', 'PersonCode'],['User','UserID_KF'],['Adgroup','AdgroupID']]

    for i in info_list:
        returngoods_list = cond_data(returngoods_list, i)

    return returngoods_list


