# coding=utf-8
import re

from program import Handle
from program import Saleout_eb
from logger import put_meiqia,post_meiqia
from program import data_query
from program import Person

B={'北京市': '010', '上海市': '021', '天津市': '022', '重庆市': '023', '合肥市': '0551', '芜湖市': '0553', '安庆市': '0556', '蚌埠市': '0552', '亳州市': '0558', '巢湖市': '0565', '池州市': '0566', '滁州市': '0550', '阜阳市': '0558', '黄山市': '0559', '淮北市': '0561', '淮南市': '0554', '六安市': '0564', '马鞍山市': '0555', '宿州市': '0557', '铜陵市': '0562', '宣城市': '0563', '福州市': '0591', '厦门市': '0592', '泉州市': '0595', '龙岩市': '0597', '宁德市': '0593', '南平市': '0599', '莆田市': '0594', '三明市': '0598', '漳州市': '0596', '兰州市': '0931', '白银市': '0943', '定西市': '0932', '金昌市': '0935', '酒泉市': '0937', '平凉市': '0933', '庆阳市': '0934', '武威市': '0935', '天水市': '0938', '张掖市': '0936', '甘南藏族自治州市': '0941', '嘉峪关市': '0937', '临夏回族自治州市': '0930', '陇南市': '2935', '广州市': '020', '深圳市': '0755', '珠海市': '0756', '东莞市': '0769', '佛山市': '0757', '惠州市': '0752', '江门市': '0750', '中山市': '0760', '汕头市': '0754', '湛江市': '0759', '潮州市': '0768', '河源市': '0762', '揭阳市': '0663', '茂名市': '0668', '梅州市': '0753', '清远市': '0763', '韶关市': '0751', '汕尾市': '0660', '阳江市': '0662', '云浮市': '0766', '肇庆市': '0758', '南宁市': '0771', '北海市': '0779', '防城港市': '0770', '桂林市': '0773', '柳州市': '0772', '崇左市': '0771', '来宾市': '0772', '梧州市': '0774', '河池市': '0778', '玉林市': '0775', '贵港市': '0755', '贺州市': '0774', '钦州市': '0777', '百色市': '0776', '贵阳市': '0851', '安顺市': '0851', '遵义市': '0851', '六盘水市': '0858', '毕节市': '0857', '黔东南苗族侗族自治州市': '0855', '黔西南布依族苗族自治州市': '0859', '黔南布依族苗族自治州市': '0854', '铜仁市': '0856', '海口市': '0898', '三亚市': '0898', '白沙黎族自治县': '0898', '保亭黎族苗族自治县': '0898', '昌江黎族自治县': '0898', '澄迈县': '0898', '定安县': '0898', '东方市': '0898', '乐东黎族自治县': '0898', '临高县': '0898', '陵水黎族自治县': '0898', '琼海市': '0898', '琼中黎族苗族自治县': '0898', '屯昌县': '0898', '万宁市': '0898', '文昌市': '0898', '五指山市': '0898', '儋州市': '0898', '石家庄市': '0311', '保定市': '0312', '承德市': '0314', '邯郸市': '0310', '唐山市': '0315', '秦皇岛市': '0335', '沧州市': '0317', '衡水市': '0318', '廊坊市': '0316', '邢台市': '0319', '张家口市': '0313', '郑州市': '0371', '洛阳市': '0379', '开封市': '0371', '许昌市': '0374', '安阳市': '0372', '平顶山市': '0375', '鹤壁市': '0392', '焦作市': '0391', '济源市': '0391', '漯河市': '0395', '南阳市': '0377', '濮阳市': '0393', '三门峡市': '0398', '商丘市': '0370', '新乡市': '0373', '信阳市': '0376', '驻马店市': '0396', '周口市': '0394', '哈尔滨市': '0451', '大庆市': '0459', '齐齐哈尔市': '0452', '佳木斯市': '0454', '大兴安岭市': '0457', '黑河市': '0456', '鹤岗市': '0468', '鸡西市': '0467', '牡丹江市': '0453', '七台河市': '0464', '绥化市': '0455', '双鸭山市': '0469', '伊春市': '0458', '武汉市': '027', '襄阳市': '0710', '十堰市': '0719', '黄石市': '0714', '鄂州市': '0711', '恩施市': '0718', '黄冈市': '0713', '荆州市': '0716', '荆门市': '0724', '随州市': '0722', '宜昌市': '0717', '天门市': '0728', '潜江市': '0728', '仙桃市': '0728', '孝感市': '0712', '咸宁市': '0715', '神农架林区': '0719', '长沙市': '0731', '岳阳市': '0730', '湘潭市': '0731', '常德市': '0736', '郴州市': '0735', '衡阳市': '0734', '怀化市': '0745', '娄底市': '0738', '邵阳市': '0739', '益阳市': '0737', '永州市': '0746', '株洲市': '0731', '张家界市': '0744', '湘西土家族苗族自治州市': '0743', '长春市': '0431', '吉林市': '0432', '延边朝鲜族自治州市': '0433', '白城市': '0436', '白山市': '0439', '辽源市': '0437', '四平市': '0434', '松原市': '0438', '通化市': '0435', '南京市': '025', '苏州市': '0512', '常州市': '0519', '连云港市': '0518', '泰州市': '0523', '无锡市': '0510', '徐州市': '0516', '扬州市': '0514', '镇江市': '0511', '淮安市': '0517', '南通市': '0513', '宿迁市': '0527', '盐城市': '0515', '南昌市': '0791', '赣州市': '0797', '九江市': '0792', '景德镇市': '0798', '吉安市': '0796', '萍乡市': '0799', '上饶市': '0793', '新余市': '0790', '宜春市': '0795', '鹰潭市': '0701', '抚州市': '0794', '沈阳市': '024', '大连市': '0411', '鞍山市': '0412', '丹东市': '0415', '抚顺市': '024', '锦州市': '0416', '营口市': '0417', '本溪市': '024', '朝阳市': '0421', '阜新市': '0418', '葫芦岛市': '0429', '辽阳市': '0419', '盘锦市': '0427', '铁岭市': '024', '呼和浩特市': '0471', '包头市': '0472', '赤峰市': '0476', '鄂尔多斯市': '0477', '乌兰察布市': '0474', '乌海市': '0473', '兴安盟市': '0482', '呼伦贝尔市': '0470', '通辽市': '0475', '阿拉善盟市': '0483', '巴彦淖尔市': '0478', '锡林郭勒市': '0479', '银川市': '0951', '石嘴山市': '0952', '固原市': '0954', '吴忠市': '0953', '中卫市': '0955', '西宁市': '0971', '黄南藏族自治州市': '0973', '玉树藏族自治州市': '0976', '果洛藏族自治州市': '0975', '海东市': '0972', '海西市': '0977', '海南藏族自治州市': '0974', '海北市': '0970', '济南市': '0531', '青岛市': '0532', '威海市': '0631', '烟台市': '0535', '潍坊市': '0536', '泰安市': '0538', '滨州市': '0543', '德州市': '0534', '东营市': '0546', '菏泽市': '0530', '济宁市': '0537', '聊城市': '0635', '临沂市': '0539', '莱芜市': '0634', '日照市': '0633', '淄博市': '0533', '枣庄市': '0632', '太原市': '0351', '长治市': '0355', '大同市': '0352', '晋城市': '0356', '晋中市': '0354', '临汾市': '0357', '吕梁市': '0358', '朔州市': '0349', '忻州市': '0350', '运城市': '0359', '阳泉市': '0353', '西安市': '029', '安康市': '0915', '宝鸡市': '0917', '汉中市': '0916', '商洛市': '0914', '铜川市': '0919', '渭南市': '0913', '咸阳市': '029', '延安市': '0911', '榆林市': '0912', '成都市': '028', '绵阳市': '0816', '资阳市': '028', '巴中市': '0827', '德阳市': '0838', '达州市': '0818', '广安市': '0826', '广元市': '0839', '乐山市': '0833', '泸州市': '0830', '眉山市': '028', '内江市': '0832', '南充市': '0817', '攀枝花市': '0812', '遂宁市': '0825', '宜宾市': '0831', '雅安市': '0835', '自贡市': '0813', '阿坝藏族羌族自治州市': '0837', '甘孜藏族自治州市': '0836', '凉山彝族自治州市': '0834', '拉萨市': '0891', '阿里市': '0897', '昌都市': '0895', '林芝市': '0894', '那曲市': '0896', '山南市': '0893', '乌鲁木齐市': '0991', '石河子市': '0993', '吐鲁番市': '0995', '伊犁市': '0999', '阿克苏市': '0997', '阿勒泰市': '0906', '巴音市': '0996', '博尔塔拉市': '0909', '昌吉市': '0994', '哈密市': '0902', '和田市': '0903', '喀什市': '0998', '克拉玛依市': '0990', '克孜勒市': '0908', '塔城市': '0901', '昆明市': '0871', '玉溪市': '0877', '楚雄彝族自治州市': '0878', '大理白族自治州市': '0872', '红河哈尼族彝族自治州市': '0873', '曲靖市': '0874', '西双版纳市': '0691', '昭通市': '0870', '保山市': '0875', '德宏市': '0692', '迪庆藏族自治州市': '0887', '丽江市': '0888', '临沧市': '0883', '怒江僳僳族自治州市': '0886', '普洱市': '0879', '文山壮族苗族自治州市': '0876', '杭州市': '0571', '宁波市': '0574', '嘉兴市': '0573', '绍兴市': '0575', '温州市': '0577', '舟山市': '0580', '湖州市': '0572', '金华市': '0579', '丽水市': '0578', '台州市': '0576', '衢州市': '0570', '香港特别行政区': '+852', '澳门特别行政区': '+853'}

def revise_data(re_data):

    revise_data = re_data
    revise_url = '/api/v1.0/one/dsl/query?dsl={"Tickets_ReturnGoods":{"fields":"id","cond":{"==":{"XSNumbers":"' + revise_data['code'] + '"}}}}'
    revise_id = post_meiqia(revise_url)
    if revise_id:
        rev_url = '/api/v1.0/one/Tickets_ReturnGoods/'+revise_id[0]['id']
        revise_data['version'] = revise_id[0]['version']
        put_meiqia(revise_data,rev_url)

class Data():
    def __init__(self,data):

        self.data = data

    def customer(self):
        url = "/api/v1.0/one/Channel/"
        data = self.data['customer']
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
            data_query(dict_c, "Channel", url, 'channel_name')

    def saleorderlist(self):
        url = "/api/v1.0/one/OrderInfo/"
        data = self.data['saleorderlist']
        for i in data:
            dict_s = {}
            dict_s['name'] = i['code']  # 订单号
            dict_s['OrderTime'] = i['date'] + "T00:00:00Z"  # 日期
            dict_s['BusinessType'] = i['businesstype']  # 业务类型
            dict_s['TypeCode'] = i['typecode']  # 销售类型编码
            dict_s['TypeName'] = i['typename']  # 销售类型
            dict_s['State'] = i['state']  # 单据状态
            dict_s['Custcode'] = i['custcode']  # 客户编码
            dict_s['Cusname'] = i['cusname']  # 客户名称
            dict_s['Cusabbname'] = i['cusabbname']  # 客户简称
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
            data_query(dict_s, "OrderInfo", url, 'name')

    def inventory(self):
        url = "/api/v1.0/one/Product/"
        data = self.data['inventory']
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
            if 'ref_sale_price' in i:
                dict_i['Price'] = float(i['ref_sale_price'])  # 单价
            if 'bbarcode' in i:
                dict_i['Bbarcode'] = i['bbarcode']  # 条形码管理
            if 'defwarehousename' in i:
                dict_i['Defwarehousename'] = i['defwarehousename']  # 默认仓库名称
            if 'defwarehouse' in i:
                dict_i['Defwarehouse'] = i['defwarehouse']  # 默认仓库
            if 'sale_flag' in i:
                if i['sale_flag'] == "1":
                    dict_i['SaleFlag'] = "是"  # 是否内销
                else:
                    dict_i["SaleFlag"] = "否"
            if 'bexpsale' in i:
                if i['bexpsale'] == "1":  # 是否外销
                    dict_i['Bexpsale'] = "是"
                else:
                    dict_i['Bexpsale'] = "否"
            if 'entry' in i:
                if 'invcode' in i['entry'][0]:
                    dict_i['Entry'] = i['entry'][0]['invcode']  # 存货编码
                if 'partid' in i['entry'][0]:
                    dict_i['Partid'] = i['entry'][0]['partid']
            # data_query(dict_i, "Product", url, 'ProductNumber')

    def person(self):
        url = "/api/v1.0/one/Salesman/"
        data = self.data['person']

        for i in data:
            dict_p = {}
            dict_p["name"] = i["name"]
            dict_p["PersonnelNumber"] = i["code"]
            dict_p["DepartmentName"] = i["cdept_name"]
            dict_p["DepartmentCode"] = i["cdept_num"]
            if 'rEmployState' in i:
                if i["rEmployState"] == "10":
                    dict_p["Employment_status"] = "在职"
                    Person(dict_p).incumbency()
                elif i["rEmployState"] == "20":
                    dict_p["Employment_status"] =  "离退"
                    Person(dict_p).retreat()
                elif i["rEmployState"] == "30":
                    dict_p["Employment_status"] = "离职"
                    Person(dict_p).retreat()

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
                if i['receiver_mobile']:
                    if len(i['receiver_mobile']) <=12:
                        if i['receiver_mobile'].startswith('1'):
                            phone_pat = '^((13[0-9])|(14[5,7])|(15[0-3,5-9])|(17[0,3,5-8])|(18[0-9])|166|198|199|(147))\\d{8}$'
                            if re.search(phone_pat,i['receiver_mobile']):
                                list_e['Phone'] = "+86 " + i['receiver_mobile']
                            else:
                                list_e['Remarks'] = "电话号码:" + i['receiver_mobile']
                        elif i['receiver_mobile'].startswith('0'):
                            if '-' in i['receiver_mobile']:
                                phe = i['receiver_mobile'].split('-')
                                list_e['Phone'] = '+86 '+ phe[0] + phe[1]
                            elif '-' not in i['receiver_mobile'] and len(i['receiver_mobile']) == 11 :
                                list_e['Phone'] = "+86 " + i['receiver_mobile']
                            else:
                                list_e['Remarks'] = "电话号码:" + i['receiver_mobile']
                        else :
                            if re.search('^[1-9]{1}[0-9]{5,8}$',i['receiver_mobile']):

                                if re.search(i['receiver_city'],str(B.keys())) :
                                    list_e['Phone'] = "+86 " + B[i['receiver_city']] + i['receiver_mobile']
                                else:
                                    list_e['Remarks'] = "电话号码:" + i['receiver_mobile']
                            else:
                                list_e['Remarks'] = "电话号码:" + i['receiver_mobile']

                    else:
                        list_e['Remarks'] = "电话号码:" + i['receiver_mobile']
            if 'tid' in i:
                list_e['TransactionNumber'] = i['tid']

            Saleout_eb(list_e).execution()

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
                # revise_data(list_a)

            Saleout_eb(list_s).execution()