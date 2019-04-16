# -*- coding:utf-8 -*-

try:
    import xml.etree.cElementTree as et
except ImportError:
    import xml.etree.ElementTree as et

from web_interface import Web_interface
from public_method import Method,analy_data,loger

product = {}

def analysis_product(data):

    data = et.fromstring(data)

    if data:
        for i in data:
            try:
                dict_p = {}

                if i.find('dEDate') != None and i.find('dEDate').text:#停用日期
                    dict_p['status'] = '停用'

                dict_p['name'] = i.find('cInvName').text #存货名称
                dict_p['ProductNumber'] = i.find('cInvCode').text #存货编码
                dict_p['Specs'] = i.find('cInvStd').text #规格型号
                dict_p['ProductSortCode'] = i.find('cInvCCode').text #产品所属分类码
                dict_p['ProductSortName'] = i.find('cInvCName').text #产品分类名称
                dict_p['MainMeasure'] = i.find('cComUnitCode').text #主计量单位编码
                dict_p['Unit'] = i.find('cComUnitName').text #主计量单位名称
                dict_p['Bbarcode'] = i.find('cInvAddCode').text #存货代码(条形码)
                if i.find('bService').text:#是否应税劳务
                    if i.find('bService').text == '0':
                        dict_p['taxable_services'] = '否'
                    else:
                        dict_p['taxable_services'] = '是'
                dict_p['WarrantyPeriod'] = int(i.find('iWarrantyPeriod').text) #保修期限
                dict_p['Imptaxrate'] = float(i.find('iImpTaxRate').text)/100 #进项税率
                dict_p['TaxRate'] = float(i.find('iTaxRate').text)/100 #销项税率
                dict_p['web_create_time'] = i.find('dInvCreateDatetime').text + 'Z' #建档日期
                dict_p['web_modify_time'] = i.find('dModifyDate').text + 'Z' #修改日期
                dict_p['TaxUnitPrice'] = float(i.find('iInvSCost').text) #单价
                dict_p['ProductVolume'] = float(i.find('iVolume').text) #体积
                dict_p['Defwarehouse'] = i.find('cDefWareHouse').text #仓库编码
                dict_p['Defwarehousename'] = i.find('cWhName').text #仓库名称
                dict_p['is_gift'] = i.find('cInvDefine7').text #是否允许赠品
                dict_p['GrossWeight'] = float(i.find('fGrossW').text) #毛重
                dict_p['NetWeight'] = float(i.find('iinvweight').text) #净重
                product[i.find('cInvCode').text] = dict_p
                print(dict_p)
            except Exception as error:
                loger().info(error)




#主程序
def main():

    web_product = Web_interface().product_info()

    if not web_product:
        i = 1
        while i <= 3:

            web_data = Web_interface().product_info()
            if web_data:

                analysis_product(web_product)
                break
            i += 1
    else:
        analysis_product(web_product)

    list_product = list(product.values())
    analy_sn = analy_data(list_product)
    for i in analy_sn:

        url = "https://crm.meiqia.com/api/v1.0/one/Product/"
        Method(url,{'objects':i}).post_data()


if __name__ == '__main__':
    main()