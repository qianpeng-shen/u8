# coding=utf-8
import re

from phone import Phone

from processing import Handle
from processing import Saleout_eb
from logger import post_meiqia,put_meiqia


def revise_data(re_data):

    revise_data = re_data
    revise_url = '/api/v1.0/one/dsl/query?dsl={"Tickets_ReturnGoods":{"fields":"id","cond":{"==":{"XSNumbers":"' + revise_data['code'] + '"}}}}'
    revise_id = post_meiqia(revise_url)
    if revise_id:
        rev_url = '/api/v1.0/one/Tickets_ReturnGoods/'+revise_id[0]['id']
        revise_data['version'] = revise_id[0]['version']
        put_meiqia(revise_data,rev_url)

class Information():
    def __init__(self,data):

        self.data = data

    def customer(self):
        url = "/api/v1.0/one/Channel/"
        data = self.data['customer']
        list_c = []
        for i in data:
            dict_c = {}
            dict_c['name'] = i['name']  # 购买渠道编码
            dict_c['channel_name'] = i['code'] #购买渠道名称
            if 'address' in i:
                dict_c['ChannelAddress'] = i['address']  # 联系地址
            if 'contact' in i:
                dict_c['ChannelContact'] = i['contact']  # 联系人
            # 考虑手机号和电话的情况
            if 'mobile' in i or 'phone' in i:
                if 'mobile' in i and 'phone' in i:
                    if i['mobile'] and i['phone']:
                        if i['mobile'] == i['phone']:
                            if len(i['mobile']) == 11:
                                dict_c['ChannelPhone'] = "+86 " + i['mobile']
                            elif len(i['mobile']) == 12 and "-" in i['mobile']:
                                dic = i['phone'].split("-")
                                dict_c['ChannelPhone'] = "+86 " + dic[0] + dic[1]
                            elif len(i['mobile']) > 11 and "-" not in i['mobile']:
                                dict_c['Remarks'] = i['mobile']

                        elif i['mobile'] != i['phone']:
                            if len(i['mobile']) == 11:
                                dict_c['ChannelPhone'] = "+86 " + i['mobile']
                                dict_c['Remarks'] = i['phone']
                            elif len(i['mobile']) > 11:
                                aa = '(13\d|14[5|7]|15\d|166|17[3|6|7]|18\d)\d{8}'
                                dit = re.search(aa, i['mobile']).group()
                                dict_c['name'] = '+86 ' + dit
                                dict_c['Remarks'] = i['mobile'] + i['phone']

                    elif i['phone'] and not i['mobile']:
                        Handle(dict_c, i['phone']).get_phone()
                    elif i['mobile'] and not i['phone']:
                        Handle(dict_c, i['mobile']).get_mobile()

                elif 'mobile' in i and 'phone' not in i:
                    if i['mobile']:
                        Handle(dict_c, i['mobile']).get_mobile()
                elif 'mobile' not in i and 'phone' in i:
                    if i['phone']:
                        Handle(dict_c, i['phone']).get_phone()
            list_c.append(dict_c)

        payload = {"objects": list_c}
        post_meiqia(url, payload)

    def saleorderlist(self):
        url = "/api/v1.0/one/OrderInfo/"
        data = self.data['saleorderlist']
        list_s = []
        for i in data:
            dict_s = {}
            dict_s['name'] = i['code']  # 订单号
            dict_s['OrderTime'] = i['date'] + "T00:00:00Z"  # 日期
            dict_s['BusinessType'] = i['businesstype']  # 业务类型
            dict_s['TypeCode'] = i['typecode']  # 销售类型编码
            dict_s['TypeName'] = i['typename']  # 销售类型
            dict_s['State'] = i['state']  # 单据状态
            dict_s['Custcode'] = i['custcode']  # 客户编码
            if 'cusname' in i :
                cusname = Handle(i['cusname'],'Channel').get_id()
                if cusname:
                    dict_s['Cusname'] = cusname  # 客户名称
            if 'cusabbname' in i :
                cusa = Handle(i['cusabbname'],'Channel').get_id()
                if cusa:
                    dict_s['Cusabbname'] = cusa  # 客户简称
            dict_s['Deptcode'] = i['deptcode']  # 部门编码
            dict_s['Deptname'] = i['deptname']  # 部门名称
            if 'personcode' in i:
                dict_s['Personcode'] = i['personcode']  # 人员编码
            if 'personname' in i:
                dict_s['PersonName'] = i['personname']  # 人员
            if 'sendaddress' in i:
                dict_s['Sendaddress'] = i['sendaddress']  # 发货地址
            dict_s['Dpremodatebt'] = i['dpremodatebt'] + "T15:04:05Z"  # 预完工日期
            dict_s['Dpredatebt'] = i['dpredatebt'] + "T15:04:05Z"  # 预发货日期
            dict_s['Maker'] = i['maker']  # 制单人
            dict_s['Money'] = float(i['money'])  # 无税金额
            dict_s['Sum'] = float(i['sum'])  # 价税合计
            if 'createsystime' in i:  # 系统创建时间
                dict_s['Createsystime'] = i['createsystime'].split(" ")[0] + "T" + \
                                          i['createsystime'].split(" ")[1].split(".")[0] + "Z"
            if 'verifysystime' in i:
                dict_s['Verifysystime'] = i['verifysystime'].split(" ")[0] + "T" + \
                                          i['verifysystime'].split(" ")[1].split(".")[0] + "Z"
            if 'verifier' in i:
                dict_s['Verifier'] = i['verifier']  # 审核人
            if 'define14' in i:
                dict_s['Define14'] = i['define14']  # 地址
            if 'define9' in i:
                dict_s['Define9'] = i['define9']
            if 'define10' in i:
                dict_s['Define10'] = i['define10']
            if 'define13' in i:
                dict_s['Define13'] = i['define13']
            if 'define11' in i:
                dict_s['Define11'] = i['define11']
            if 'define16' in i:
                dict_s['Define16'] = i['define16']
            if 'fhstatus' in i:  # 发货状态(0=未发货;1=部分发货;2=全部发货)
                if i['fhstatus'] == "0":
                    dict_s['Fhstatus'] = "未发货"
                elif i['fhstatus'] == "1":
                    dict_s['Fhstatus'] = "部分发货"
                else:
                    dict_s['Fhstatus'] = "全部发货"
            list_s.append(dict_s)
        payload = {"objects": list_s}
        post_meiqia(url, payload)
    def inventory(self):
        url = "/api/v1.0/one/Product/"
        data = self.data['inventory']
        list_i = []
        for i in data:
            dict_i = {}
            if 'end_date' in i:
                if i['end_date']:
                    continue
            if 'self_define1' in i:
                dict_i['self_define1'] = i['self_define1']
            dict_i['ProductNumber'] = i['code']  # 产品编码
            if 'fRetailPrice' in i:
                dict_i['TaxUnitPrice'] = float(i['fRetailPrice'])  # 含税单价
            dict_i['name'] = i['name']  # 存货名称
            if "specs" in i:
                dict_i['Specs'] = i['specs']  # 规格型号
            dict_i['ProductSortCode'] = i['sort_code']  # 所属分类码
            dict_i['ProductSortName'] = i['sort_name']  # 所属分类名称
            dict_i['MainMeasure'] = i['main_measure']  # 主计量单位
            dict_i['Unit'] = i['ccomunitname']  # 单位
            dict_i['StartDate'] = i['start_date'].split(" ")[0] + "T" + \
                                  i['start_date'].split(" ")[1].split(".")[0] + "Z"  # 启用时间
            if 'modifydate' in i:
                dict_i['ModifyDate'] = i['modifydate'].split(" ")[0] + "T" + \
                                       i['modifydate'].split(" ")[1].split(".")[0] + "Z"  # 变更时间
            if 'isupplytype' in i:
                dict_i['ProductIsupplyType'] = i['isupplytype']  # 供应类型
            dict_i['Imptaxrate'] = float(i['iimptaxrate']) / 100  # 进项税率
            dict_i['TaxRate'] = float(i['tax_rate']) / 100  # 销售税率
            if 'bbarcode' in i:
                dict_i['Bbarcode'] = i['bbarcode']  # 条形码管理
            if 'defwarehousename' in i:
                dict_i['Defwarehousename'] = i['defwarehousename']  # 默认仓库名称
            if 'defwarehouse' in i:
                dict_i['Defwarehouse'] = i['defwarehouse']  # 默认仓库
            if 'entry' in i:
                if 'partid' in i['entry'][0]:
                    dict_i['Partid'] = i['entry'][0]['partid']

            list_i.append(dict_i)
        payload = {"objects": list_i}
        post_meiqia(url, payload)
    def person(self):
        url = "/api/v1.0/one/Salesman/"
        data = self.data['person']
        # print(data)
        list_p = []
        for i in data:
            dict_p = {}
            dict_p["name"] = i["name"]
            dict_p["PersonnelNumber"] = i["code"]
            dict_p["DepartmentName"] = i["cdept_name"]
            dict_p["DepartmentCode"] = i["cdept_num"]
            list_p.append(dict_p)
        payload = {"objects": list_p}
        post_meiqia(url, payload)
    def eb_tradelist(self):
        data = self.data['eb_tradelist']
        for i in data:
            list_e = {}
            if 'cshipcode' not in i:
                continue
            if 'cshipcode' in i:
                if i['cshipcode']:
                    if 'FHXS' in i['cshipcode']:
                        eb_data = Saleout_eb(i['cshipcode'].split('H')[1]).eb_query()
                        if eb_data:
                            list_e['code'] = eb_data['id']
                            list_e['version'] = eb_data['version']
                        else:
                            continue
                    elif 'XS' not in i['cshipcode'] and 'FH' in i['cshipcode']:
                        eb_data = Saleout_eb('XS' + i['cshipcode'].split('H')[1]).eb_query()
                        if eb_data:
                            list_e['code'] = eb_data['id']
                            list_e['version'] = eb_data['version']
                        else:
                            continue
                    else:
                        eb_data = Saleout_eb(i['cshipcode']).eb_query()
                        if eb_data:
                            list_e['code'] = eb_data['id']
                            list_e['version'] = eb_data['version']
                        else:
                            continue
                else:
                    continue
            if 'receiver_name' in i:
                list_e['ConsigneeNam'] = i['receiver_name']
            if 'receiver_state' in i:
                if len(i['receiver_state']) == 2:
                    if i['receiver_state'] in ['北京', '天津', '上海', '重庆']:
                        state_id = Handle(i['receiver_state'] + '市',"Province").get_id()
                        if state_id:
                            list_e['Cprovince'] = state_id[0]['id']
                    else:
                        state_id = Handle(i['receiver_state'] + '省',"Province").get_id()
                        if state_id:
                            list_e['Cprovince'] = state_id[0]['id']
                else:
                    state_id = Handle(i['receiver_state'],"Province").get_id()
                    if state_id:
                        list_e['Cprovince'] = state_id[0]['id']
            if 'receiver_city' in i:

                if "市" in i['receiver_city']:
                    city_id = Handle(i['receiver_city'],"Municipality").get_id()
                    if city_id:
                        list_e['Scity'] = city_id[0]['id']

                else:
                    city_id = Handle(i['receiver_city'] + '市',"Municipality").get_id()
                    if city_id:
                        list_e['Scity'] = city_id[0]['id']

            if 'receiver_district' in i:

                dis_id = Handle(i['receiver_district'],"Prefecture").get_id()
                if dis_id:
                    list_e['Cdistrict'] = dis_id[0]['id']

            if 'receiver_address' in i:
                list_e['Address'] = i['receiver_address']
            if 'receiver_mobile' in i:
                if 7 <= len(i['receiver_mobile']) <= 11:
                    if Phone().find(i['receiver_mobile']):
                        list_e['Phone'] = "+86 " + i['receiver_mobile']
                    else:
                        list_e['Remarks'] = "电话号码:" + i['receiver_mobile']
                else:
                    list_e['Remarks'] = "电话号码:" + i['receiver_mobile']

            # Saleout_eb(list_e).execution()

    def saleoutlistall(self):

        data = self.data['saleoutlistall']
        for i in data:
            list_s = {}
            list_a = {}
            if 'subordercode' not in i:
                continue
            if 'subordercode' in i:
                if i['subordercode']:
                    sale = Saleout_eb(i['subordercode']).saleout_query()
                    if sale:
                        list_s['code'] = sale['id']
                        list_s['version'] = sale['version']
                        if sale['LogisticsNumber']:
                            if 'subconsignmentcode' in i:
                                list_s['LogisticsNumber'] = sale['LogisticsNumber'] + ';' + i['subconsignmentcode']
                    else:
                        continue
                else:
                    continue

            if 'quantity' in i:
                if float(i['quantity']) <= 0:
                    list_a['code']=i['subordercode']
                    list_a['IsNotEntrepot'] = True
                revise_data(list_a)

            Saleout_eb(list_s).execution()