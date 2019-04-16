# -*- coding:utf-8 -*-
import re
try:
    import xml.etree.cElementTree as et
except ImportError:
    import xml.etree.ElementTree as et

from web_interface import Web_interface
from public_method import Method,analy_data,loger,cond_data

B={'北京市': '010', '上海市': '021', '天津市': '022', '重庆市': '023', '合肥市': '0551', '芜湖市': '0553', '安庆市': '0556', '蚌埠市': '0552', '亳州市': '0558', '巢湖市': '0565', '池州市': '0566', '滁州市': '0550', '阜阳市': '0558', '黄山市': '0559', '淮北市': '0561', '淮南市': '0554', '六安市': '0564', '马鞍山市': '0555', '宿州市': '0557', '铜陵市': '0562', '宣城市': '0563', '福州市': '0591', '厦门市': '0592', '泉州市': '0595', '龙岩市': '0597', '宁德市': '0593', '南平市': '0599', '莆田市': '0594', '三明市': '0598', '漳州市': '0596', '兰州市': '0931', '白银市': '0943', '定西市': '0932', '金昌市': '0935', '酒泉市': '0937', '平凉市': '0933', '庆阳市': '0934', '武威市': '0935', '天水市': '0938', '张掖市': '0936', '甘南藏族自治州市': '0941', '嘉峪关市': '0937', '临夏回族自治州市': '0930', '陇南市': '2935', '广州市': '020', '深圳市': '0755', '珠海市': '0756', '东莞市': '0769', '佛山市': '0757', '惠州市': '0752', '江门市': '0750', '中山市': '0760', '汕头市': '0754', '湛江市': '0759', '潮州市': '0768', '河源市': '0762', '揭阳市': '0663', '茂名市': '0668', '梅州市': '0753', '清远市': '0763', '韶关市': '0751', '汕尾市': '0660', '阳江市': '0662', '云浮市': '0766', '肇庆市': '0758', '南宁市': '0771', '北海市': '0779', '防城港市': '0770', '桂林市': '0773', '柳州市': '0772', '崇左市': '0771', '来宾市': '0772', '梧州市': '0774', '河池市': '0778', '玉林市': '0775', '贵港市': '0755', '贺州市': '0774', '钦州市': '0777', '百色市': '0776', '贵阳市': '0851', '安顺市': '0851', '遵义市': '0851', '六盘水市': '0858', '毕节市': '0857', '黔东南苗族侗族自治州市': '0855', '黔西南布依族苗族自治州市': '0859', '黔南布依族苗族自治州市': '0854', '铜仁市': '0856', '海口市': '0898', '三亚市': '0898', '白沙黎族自治县': '0898', '保亭黎族苗族自治县': '0898', '昌江黎族自治县': '0898', '澄迈县': '0898', '定安县': '0898', '东方市': '0898', '乐东黎族自治县': '0898', '临高县': '0898', '陵水黎族自治县': '0898', '琼海市': '0898', '琼中黎族苗族自治县': '0898', '屯昌县': '0898', '万宁市': '0898', '文昌市': '0898', '五指山市': '0898', '儋州市': '0898', '石家庄市': '0311', '保定市': '0312', '承德市': '0314', '邯郸市': '0310', '唐山市': '0315', '秦皇岛市': '0335', '沧州市': '0317', '衡水市': '0318', '廊坊市': '0316', '邢台市': '0319', '张家口市': '0313', '郑州市': '0371', '洛阳市': '0379', '开封市': '0371', '许昌市': '0374', '安阳市': '0372', '平顶山市': '0375', '鹤壁市': '0392', '焦作市': '0391', '济源市': '0391', '漯河市': '0395', '南阳市': '0377', '濮阳市': '0393', '三门峡市': '0398', '商丘市': '0370', '新乡市': '0373', '信阳市': '0376', '驻马店市': '0396', '周口市': '0394', '哈尔滨市': '0451', '大庆市': '0459', '齐齐哈尔市': '0452', '佳木斯市': '0454', '大兴安岭市': '0457', '黑河市': '0456', '鹤岗市': '0468', '鸡西市': '0467', '牡丹江市': '0453', '七台河市': '0464', '绥化市': '0455', '双鸭山市': '0469', '伊春市': '0458', '武汉市': '027', '襄阳市': '0710', '十堰市': '0719', '黄石市': '0714', '鄂州市': '0711', '恩施市': '0718', '黄冈市': '0713', '荆州市': '0716', '荆门市': '0724', '随州市': '0722', '宜昌市': '0717', '天门市': '0728', '潜江市': '0728', '仙桃市': '0728', '孝感市': '0712', '咸宁市': '0715', '神农架林区': '0719', '长沙市': '0731', '岳阳市': '0730', '湘潭市': '0731', '常德市': '0736', '郴州市': '0735', '衡阳市': '0734', '怀化市': '0745', '娄底市': '0738', '邵阳市': '0739', '益阳市': '0737', '永州市': '0746', '株洲市': '0731', '张家界市': '0744', '湘西土家族苗族自治州市': '0743', '长春市': '0431', '吉林市': '0432', '延边朝鲜族自治州市': '0433', '白城市': '0436', '白山市': '0439', '辽源市': '0437', '四平市': '0434', '松原市': '0438', '通化市': '0435', '南京市': '025', '苏州市': '0512', '常州市': '0519', '连云港市': '0518', '泰州市': '0523', '无锡市': '0510', '徐州市': '0516', '扬州市': '0514', '镇江市': '0511', '淮安市': '0517', '南通市': '0513', '宿迁市': '0527', '盐城市': '0515', '南昌市': '0791', '赣州市': '0797', '九江市': '0792', '景德镇市': '0798', '吉安市': '0796', '萍乡市': '0799', '上饶市': '0793', '新余市': '0790', '宜春市': '0795', '鹰潭市': '0701', '抚州市': '0794', '沈阳市': '024', '大连市': '0411', '鞍山市': '0412', '丹东市': '0415', '抚顺市': '024', '锦州市': '0416', '营口市': '0417', '本溪市': '024', '朝阳市': '0421', '阜新市': '0418', '葫芦岛市': '0429', '辽阳市': '0419', '盘锦市': '0427', '铁岭市': '024', '呼和浩特市': '0471', '包头市': '0472', '赤峰市': '0476', '鄂尔多斯市': '0477', '乌兰察布市': '0474', '乌海市': '0473', '兴安盟市': '0482', '呼伦贝尔市': '0470', '通辽市': '0475', '阿拉善盟市': '0483', '巴彦淖尔市': '0478', '锡林郭勒市': '0479', '银川市': '0951', '石嘴山市': '0952', '固原市': '0954', '吴忠市': '0953', '中卫市': '0955', '西宁市': '0971', '黄南藏族自治州市': '0973', '玉树藏族自治州市': '0976', '果洛藏族自治州市': '0975', '海东市': '0972', '海西市': '0977', '海南藏族自治州市': '0974', '海北市': '0970', '济南市': '0531', '青岛市': '0532', '威海市': '0631', '烟台市': '0535', '潍坊市': '0536', '泰安市': '0538', '滨州市': '0543', '德州市': '0534', '东营市': '0546', '菏泽市': '0530', '济宁市': '0537', '聊城市': '0635', '临沂市': '0539', '莱芜市': '0634', '日照市': '0633', '淄博市': '0533', '枣庄市': '0632', '太原市': '0351', '长治市': '0355', '大同市': '0352', '晋城市': '0356', '晋中市': '0354', '临汾市': '0357', '吕梁市': '0358', '朔州市': '0349', '忻州市': '0350', '运城市': '0359', '阳泉市': '0353', '西安市': '029', '安康市': '0915', '宝鸡市': '0917', '汉中市': '0916', '商洛市': '0914', '铜川市': '0919', '渭南市': '0913', '咸阳市': '029', '延安市': '0911', '榆林市': '0912', '成都市': '028', '绵阳市': '0816', '资阳市': '028', '巴中市': '0827', '德阳市': '0838', '达州市': '0818', '广安市': '0826', '广元市': '0839', '乐山市': '0833', '泸州市': '0830', '眉山市': '028', '内江市': '0832', '南充市': '0817', '攀枝花市': '0812', '遂宁市': '0825', '宜宾市': '0831', '雅安市': '0835', '自贡市': '0813', '阿坝藏族羌族自治州市': '0837', '甘孜藏族自治州市': '0836', '凉山彝族自治州市': '0834', '拉萨市': '0891', '阿里市': '0897', '昌都市': '0895', '林芝市': '0894', '那曲市': '0896', '山南市': '0893', '乌鲁木齐市': '0991', '石河子市': '0993', '吐鲁番市': '0995', '伊犁市': '0999', '阿克苏市': '0997', '阿勒泰市': '0906', '巴音市': '0996', '博尔塔拉市': '0909', '昌吉市': '0994', '哈密市': '0902', '和田市': '0903', '喀什市': '0998', '克拉玛依市': '0990', '克孜勒市': '0908', '塔城市': '0901', '昆明市': '0871', '玉溪市': '0877', '楚雄彝族自治州市': '0878', '大理白族自治州市': '0872', '红河哈尼族彝族自治州市': '0873', '曲靖市': '0874', '西双版纳市': '0691', '昭通市': '0870', '保山市': '0875', '德宏市': '0692', '迪庆藏族自治州市': '0887', '丽江市': '0888', '临沧市': '0883', '怒江僳僳族自治州市': '0886', '普洱市': '0879', '文山壮族苗族自治州市': '0876', '杭州市': '0571', '宁波市': '0574', '嘉兴市': '0573', '绍兴市': '0575', '温州市': '0577', '舟山市': '0580', '湖州市': '0572', '金华市': '0579', '丽水市': '0578', '台州市': '0576', '衢州市': '0570', '香港特别行政区': '+852', '澳门特别行政区': '+853'}
orderinfo = []
order_sublist = []

def analysis_person(data):

    data = et.fromstring(data)

    if data:
        for i in data:
            try:
                dict_h = {}
                if i.find('dbgdatetime') != None:
                    update_date = i.find('dbgdatetime').text
                    if update_date and 'T' in update_date and '.' in update_date:

                        dict_h['Verifysystime'] = update_date + "Z" #修改时间
                # print(i.find('dcreatesystime').text)
                if i.find('dcreatesystime') != None:
                    create_date = i.find('dcreatesystime').text

                    if create_date and ' ' in create_date and '.' in create_date:
                        create_date = create_date.split(' ')
                        create_date = create_date[0] + 'T' + create_date[1]
                        create_date = create_date.split('.')
                        create_date = create_date[0] + 'Z'
                        dict_h['Createsystime'] = create_date #建档时间

                dict_h['name'] = i.find('csocode').text #销售订单号
                if i.find('cexpressconame').text and i.find('cexpresscode').text:
                    dict_h['LogisticsCompanyNumber'] = i.find('cexpressconame').text + ';' + i.find('cexpresscode').text
                # dict_h['LogisticsNumber'] = i.find('cebexpresscode').text
                dict_h['OrderID'] = i.find('id').text #主表ID
                dict_h['State'] = i.find('ivouchstate').text #单据状态
                if i.find('cstate') != None:
                    state = i.find('cstate').text
                    if state and state in ['未发货','已发货']:

                        dict_h['Fhstatus'] = i.find('cstate').text #发货状态
                dict_h['BusinessTypeCode'] = i.find('cbustypecode') #业务类型编码
                dict_h['BusinessType'] = i.find('cbustype').text #业务类型名称
                dict_h['TypeCode'] = i.find('cstcode').text #销售类型编码
                dict_h['TypeName'] = i.find('cstname').text #销售类型名称
                dict_h['OrderTime'] = i.find('ddate').text + 'Z' #销售订单日期
                dict_h['Custcode'] = i.find('ccuscode').text #客户编码
                dict_h['Cusname'] = i.find('ccusabbname').text #客户名称
                # dict_h[''] = i.find('ccusname').text #客户简称,暂时不做同步
                # dict_h[''] = i.find('ccusaddress').text #客户地址
                # dict_h[''] = i.find('ccushand').text #客户手机
                # dict_h[''] = i.find('客户电话').text #客户电话
                # dict_h[''] = i.find('ccusperson').text #客户联系人名称
                dict_h['Deptcode'] = i.find('cdepcode').text #部门编码
                dict_h['Deptname'] = i.find('cdepname').text #部门名称
                dict_h['Personcode'] = i.find('cpersoncode').text #业务员编码
                dict_h['PersonName'] = i.find('cpersonname').text #业务员名称
                dict_h[''] = i.find('caddcode').text #收货地址编码
                dict_h['Address'] = i.find('ccusoaddress').text #收货人地址
                dict_h['TransactionNumber'] = i.find('cebtrnumber').text #交易编号
                if i.find('cprovince') != None:
                    if i.find('cprovince').text:
                        province = i.find('cprovince').text
                        if len(province) == 2:
                            if province in ['北京', '天津', '上海', '重庆']:
                                dict_h['Cprovince'] = province + '市'
                            else:
                                dict_h['Cprovince'] = province + '省' #收货人省
                        else:
                            dict_h['Cprovince'] = province
                    else:
                        dict_h['Cprovince'] = 'province'
                if i.find('scity') != None:
                    if i.find('scity').text:
                        scity = i.find('scity').text
                        if  '市' not in scity:
                            dict_h['Scity'] = scity + '市'
                        else:
                            dict_h['Scity'] = scity #收货人市
                    else:
                        dict_h['Scity'] = 'scity'
                if i.find('cdistrict') != None:
                    if i.find('cdistrict').text:
                        dict_h['Cdistrict'] = i.find('cdistrict').text #收货人区
                    else:
                        dict_h['Cdistrict'] = 'cdistrict'

                dict_h['ConsigneeNam'] = i.find('cdefine11').text #收货人姓名
                if i.find('cdefine16') != None:
                    defind16 = i.find('cdefine16').text

                    if defind16:

                        if len(defind16) <= 12:

                            if defind16.startswith('1'):

                                moblie_re = '^((13[0-9])|(14[5,7])|(15[0-3,5-9])|(17[0,3,5-8])|(18[0-9])|166|198|199|(147))\\d{8}$'
                                if re.search(moblie_re,defind16):

                                    dict_h['Phone'] = "+86 " + defind16 #收货人电话
                                else:
                                    dict_h['Remarks'] = "电话号码:" + defind16
                            elif defind16.startswith('0'):

                                moblie_re = '0[1-9]\d{1,2}[-]?\d{7,8}'
                                if re.search(moblie_re,defind16):
                                    if '-' in defind16:
                                        phone = defind16.split('-')
                                        dict_h['Phone'] = "+86 " + phone[0] + phone[1]
                                    else:
                                        dict_h['Phone'] = "+86 " + defind16
                                else:
                                    dict_h['Remarks'] = "电话号码:" + defind16
                            else:

                                if re.search('^[1-9]{1}[0-9]{5,8}$',defind16) and 'Scity' in dict_h :
                                    if re.search(dict_h['Scity'], str(B.keys())):
                                        dict_h['Phone'] = "+86 " + B[dict_h['Scity']] + defind16
                                    else:
                                        dict_h['Remarks'] = "电话号码:" + defind16
                        else:
                            dict_h['Remarks'] = "电话号码:" + defind16

                dict_h['Maker'] = i.find('cmaker').text #制单人
                dict_h['Verifier'] = i.find('cverifier').text #审核人

                orderinfo.append(dict_h)
                if i.find('entry'):

                    if 'Phone' in dict_h:
                        e = i.find('entry')
                        dict_d = {}
                        dict_d['SublistID'] = e.find('isosid').text #子表id
                        dict_d['OrderID'] = e.find('id').text #主表id
                        dict_d['inventorycode'] = e.find('cinvcode').text #存货编码
                        dict_d['relatedProductID'] = e.find('cinvname').text #存货名称
                        dict_d['relatedOrderInfoID'] = i.find('csocode').text #订单号
                        if i.find('cexpressconame').text and i.find('cexpresscode').text:
                            dict_d['LogisticsCompanyNumber'] = i.find('cexpressconame').text + ';' + i.find('cexpresscode').text
                        # dict_d['LogisticsNumber'] = i.find('cebexpresscode').text
                        dict_d['relatedUserArchivesID'] = dict_h['Phone'] #电话号码
                        dict_d['UserName'] = dict_h['ConsigneeNam'] #用户
                        dict_d['invstd'] = e.find('cinvstd').text #规格
                        dict_d['unitname'] = e.find('cinvm_unit').text #单位名称
                        dict_d['isGift'] = e.find('cinvdefine7').text #是否充许赠品
                        dict_d['quantity'] = float(e.find('iquantity').text)#数量
                        dict_d['taxrate'] = float(e.find('itaxrate').text) #税率
                        dict_d['quotedprice'] = float(e.find('iquotedprice').text) #报价
                        dict_d['unitprice'] = float(e.find('iunitprice').text) #无税单价
                        dict_d['money'] = float(e.find('imoney').text) #无税金额
                        dict_d['taxunitprice'] = float(e.find('itaxunitprice').text) #含税单价
                        dict_d['TaxAmount'] = float(e.find('itax').text) #税额
                        dict_d['sum'] = float(e.find('isum').text) #价税合计
                        if e.find('bgift') != None:
                            if  e.find('bgift').text:
                                dict_d['isGift'] = e.find('bgift').text #是否赠品
                        order_sublist.append(dict_d)
                        print(dict_d)

            except Exception as error:
                loger().info(error)

#主程序
def main(data):

    web_order = Web_interface(data).order_info()

    if not web_order:
        i = 1
        while i <= 3:

            web_order = Web_interface(data).order_info()
            if web_order:

                analysis_person(web_order)
                break
            i += 1
    else:
        analysis_person(web_order)

    # info_list = [['Province','Cprovince'],['Municipality','Scity'],['Prefecture','Cdistrict'],['Channel','Cusname','Custcode','channel_code']]
    # order_values = orderinfo
    #
    # for i in info_list:
    #
    #     order_values = cond_data(order_values,i)

    # sublist_values = order_sublist
    #
    # sublist_list = [['OrderInfo','relatedOrderInfoID'],['UserArchives','relatedUserArchivesID'],['Product','relatedProductID','inventorycode','ProductNumber']]
    # for s in sublist_list:
    #     sublist_values = cond_data(sublist_values,s)
    #
    # for order in analy_data(order_values):
    #     order_url = "https://crm.meiqia.com/api/v1.0/one/OrderInfo/"
    #     Method(order_url,{'objects':order}).post_data()
    # for sublist in analy_data(sublist_values):
    #     sublist_url = "https://crm.meiqia.com/api/v1.0/one/ProductOfUser/"
    #     Method(sublist_url,{'objects':sublist}).post_data()




if __name__ == '__main__':
    # data = "where year(ddate)='2015' and month(ddate)='12'"
    # main(data)
    strwhere = ["where year(ddate)='2015' and month(ddate)='1'", "where year(ddate)='2015' and month(ddate)='2'", "where year(ddate)='2015' and month(ddate)='3'", "where year(ddate)='2015' and month(ddate)='4'", "where year(ddate)='2015' and month(ddate)='5'", "where year(ddate)='2015' and month(ddate)='6'", "where year(ddate)='2015' and month(ddate)='7'", "where year(ddate)='2015' and month(ddate)='8'", "where year(ddate)='2015' and month(ddate)='9'", "where year(ddate)='2015' and month(ddate)='10'", "where year(ddate)='2015' and month(ddate)='11'", "where year(ddate)='2015' and month(ddate)='12'", "where year(ddate)='2016' and month(ddate)='1'", "where year(ddate)='2016' and month(ddate)='2'", "where year(ddate)='2016' and month(ddate)='3'", "where year(ddate)='2016' and month(ddate)='4'", "where year(ddate)='2016' and month(ddate)='5'", "where year(ddate)='2016' and month(ddate)='6'", "where year(ddate)='2016' and month(ddate)='7'", "where year(ddate)='2016' and month(ddate)='8'", "where year(ddate)='2016' and month(ddate)='9'", "where year(ddate)='2016' and month(ddate)='10'", "where year(ddate)='2016' and month(ddate)='11'", "where year(ddate)='2016' and month(ddate)='12'", "where year(ddate)='2017' and month(ddate)='1'", "where year(ddate)='2017' and month(ddate)='2'", "where year(ddate)='2017' and month(ddate)='3'", "where year(ddate)='2017' and month(ddate)='4'", "where year(ddate)='2017' and month(ddate)='5'", "where year(ddate)='2017' and month(ddate)='6'", "where year(ddate)='2017' and month(ddate)='7'", "where year(ddate)='2017' and month(ddate)='8'", "where year(ddate)='2017' and month(ddate)='9'", "where year(ddate)='2017' and month(ddate)='10'", "where year(ddate)='2017' and month(ddate)='11'", "where year(ddate)='2017' and month(ddate)='12'", "where year(ddate)='2018' and month(ddate)='1'", "where year(ddate)='2018' and month(ddate)='2'", "where year(ddate)='2018' and month(ddate)='3'", "where year(ddate)='2018' and month(ddate)='4'", "where year(ddate)='2018' and month(ddate)='5'", "where year(ddate)='2018' and month(ddate)='6'", "where year(ddate)='2018' and month(ddate)='7'", "where year(ddate)='2018' and month(ddate)='8'", "where year(ddate)='2018' and month(ddate)='9'", "where year(ddate)='2018' and month(ddate)='10'", "where year(ddate)='2018' and month(ddate)='11'", "where year(ddate)='2018' and month(ddate)='12'", "where year(ddate)='2019' and month(ddate)='1'", "where year(ddate)='2019' and month(ddate)='2'", "where year(ddate)='2019' and month(ddate)='3'", "where year(ddate)='2019' and month(ddate)='4'", "where year(ddate)='2019' and month(ddate)='5'", "where year(ddate)='2019' and month(ddate)='6'", "where year(ddate)='2019' and month(ddate)='7'", "where year(ddate)='2019' and month(ddate)='8'", "where year(ddate)='2019' and month(ddate)='9'", "where year(ddate)='2019' and month(ddate)='10'", "where year(ddate)='2019' and month(ddate)='11'", "where year(ddate)='2019' and month(ddate)='12'"]
    for data in strwhere:

        main(data)