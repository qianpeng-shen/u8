# encoding=utf-8
import json
import os
import queue
import re
import threading
import logging
import time
import curlify
import xml.etree.ElementTree as et
from suds.client import Client
import datetime
import http.client
from urllib import request,parse
from phone import Phone
#创建两个队列

url_queue = queue.Queue()
data_queue = queue.Queue()

#创建日志文件

root_path = os.getcwd()
log_path = root_path + '/Logs'
exist_file = os.path.exists(log_path)
if not exist_file:
    os.makedirs(log_path)

logger = logging.getLogger()
logger.setLevel(logging.INFO)
rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
log_path = os.path.dirname(os.getcwd()) + '/bolebaoproject/Logs/'


log_name = log_path + rq + '.log'
logfile = log_name
fh = logging.FileHandler(logfile, mode='w', encoding='utf-8')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
fh.setFormatter(formatter)
logger.addHandler(fh)

#webservice数据处理
def get_data():
    try:
        # 前一天时间
        # end_date = datetime.date.today() - datetime.timedelta(days=1)
        # strwhere="where dckdate = '%s'"%end_date
        url = 'http://124.207.40.126:9000/YouBlbWebGw/BLBServiceGW.asmx?WSDL'
        client = Client(url)
        # print(client)
        strwhere = "where dckdate >='2018-10-01' and dckdate<='2018-10-30'"

        res = client.service.GetU8OrderData(strwhere)
        return res
    except Exception as Error:
        logger.error(Error, )

def analytic_data():
    res=get_data()
    url='/api/v1.0/one/SN/'
    root = et.fromstring(res)
    for i in root:
        root_dict = {}
        for r in i:
            pass
        payload = {'objects': [root_dict]}
        post_meiqia(payload, url)


# 获取u8token信息
class Toekn():

    def __init__(self):
        self.content_type = 'text/html'
        self.charset = 'utf-8'

    def run(self):
        url = 'https://api.yonyouup.com/system/token?from_account=bolebaokaifa&app_key=opa87ad77a2a44f12df&app_secret=7027dd0c880141308bedc8bfd0b854c9'
        request_obj = request.Request(url)
        request_obj.add_header('Content-Type', self.content_type)
        request_obj.add_header('charset', self.charset)

        json_data = request.urlopen(request_obj).read().decode()
        result = json.loads(json_data)
        if len(result) > 0:
            print('token为：', result['token']['id'])
            return result['token']['id']
        else:
            errcode = result['errcode']
            errmsg = result['errmsg']
            logger.error('获取token异常,异常码为%s，异常信息为%s' % (errcode, errmsg))
            # print('获取token异常，请重新请求')

token = Toekn().run()

# 线程类， 执行请求u8接口

#重写线程类
class ThreadYongYou(threading.Thread):

    def __init__(self, url_queue):
        threading.Thread.__init__(self)
        self.url_queue = url_queue

    # async def request(self, url):
    def request(self, url):
        dict = {}
        object = re.findall('\w+', url)[5]

        content_type = 'text/html'
        charset = 'utf-8'
        # 发起请求，并返回数据
        request_obj = request.Request(url)
        request_obj.add_header('Content-Type', content_type)
        request_obj.add_header('charset', charset)

        json_data = request.urlopen(request_obj).read().decode()
        # print(json_data)
        result = json.loads(json_data)
        dict[object] = result
        # print(self.name)
        return dict

    def run(self):
        logger.info('开始发送url请求')
        while True:
            # if url_queue.empty() == True:
            #     # print(url_queue.empty())
            #     self.url_queue.task_done()
            #     break
            url = self.url_queue.get()
            old_token = url.split('&')[3].split('=')[1]
            old_token = 'token=' + old_token
            new_token = 'token=' + token
            url = re.sub(old_token, new_token, url)

            try:
                result = ThreadYongYou.request(self, url)
                # result = loop.run_until_complete(ThreadYongYou.request(self, url))

                # 判断返回结果是否为空
                if len(result) == None:
                    logger.error('第1次请求%s异常，异常信息为：%s' % (url, result))
                    i = 1
                    while i < 3:
                        # result = loop.run_until_complete(ThreadYongYou.request(self, url))

                        result = ThreadYongYou.request(self, url)
                        if len(result) == None:
                            logger.error('第%s次请求%s异常，异常信息为：%s' %
                                         (i + 1, url, result))

                        else:
                            # (key, value), = result.items()
                            # if value['errcode'] != "0":
                            #     break
                            data_queue.put(result)
                            break
                        i += 1


                else:
                    # 添加数据到dat_queue

                    (key, value), = result.items()
                    if value['errcode'] == '0':
                        data_queue.put(result)


                    pagenum_data = re.findall(
                        r'page_index=\d+', url)[0]
                    pagenum = pagenum_data.split('=')[1]

                    if int(pagenum) == 1:
                        page = 2
                        page_count = value['page_count']
                        while int(page) <= int(page_count):
                            pages = 'page_index=' + str(page)
                            url_list = url.split('page_index=1')

                            next_url = url_list[0] + pages + url_list[1]
                            # print(next_url)
                            url_queue.put(next_url)
                            page += 1
                    # if int(pagenum) == 2749 :
                    #     page = int(pagenum) + 1
                    #     page_count = value['page_count']
                    #     while int(page) <= int(page_count):
                    #         pages = 'page_index=' + str(page)
                    #         url_list = url.split('%s' %(pagenum_data))
                    #
                    #         next_url = url_list[0] + pages + url_list[1]
                    #         url_queue.put(next_url)
                    #         page += 1
            except Exception as error:
                logger.error(error, url,)
            self.url_queue.task_done()


#执行查询插入操作
def post_meiqia(url,payload=None):
    textmod=payload
    header_dict = {
        'x-token': "AexZAHT6jVsAAEFRQUNRcXdlQWhjQkFBQUFWdFlLWGRDeFJoVlZiQUFBQVFBQ1Fxd2VYUkVCQUFBQTM1eDc2WkhsTEJVWXBRQUH-wsHHEfENv8rexZmz2t9NygV2o2Ar5FP75JgrwV8vqFwSE1mZPne4ru8o0euVwWcRg87HsXqzguyvJNiPWu2o",
        'content-type': "application/json",
        'cache-control': "no-cache",
        'postman-token': "529a9a27-2e62-0d64-aea9-c938d33ec5fd"
        }
    url = "https://crm.meiqia.com" + url
    # print(url)
    # print(textmod)
    if textmod:
        try:
            # json串数据使用
            textmod = json.dumps(textmod).encode(encoding='utf-8')
            req = request.Request(url=url, data=textmod, headers=header_dict)
            res = request.urlopen(req)
            res = res.read().decode(encoding='utf-8')
            res_data = json.loads(res)
            logging.warning(res_data)
            print(res_data)

            # if res_data['code'] != 0:
            #     res_payload = payload
            #     res_url = url
            #     post_meiqia(res_payload, res_url)

        except Exception as Error:
            # print("出错了")
            logger.error(Error)
    else:
        try:
            req = request.Request(url = url,headers = header_dict)
            res = request.urlopen(req)
            # print(res)
            res = res.read().decode(encoding = 'utf-8')
            return json.loads(res)['body']['objects']
        except Exception as Error:
            logger.error(Error)
#更改数据
def put_meiqia(payload, url):
    try:
        conn = http.client.HTTPSConnection("crm.meiqia.com")#连接指定的服务器
        payload = json.dumps(payload)
        headers = {
            'x-token': "AexZAHT6jVsAAEFRQUNRcXdlQWhjQkFBQUFWdFlLWGRDeFJoVlZiQUFBQVFBQ1Fxd2VYUkVCQUFBQTM1eDc2WkhsTEJVWXBRQUH-wsHHEfENv8rexZmz2t9NygV2o2Ar5FP75JgrwV8vqFwSE1mZPne4ru8o0euVwWcRg87HsXqzguyvJNiPWu2o",
            'content-type': "application/json",
            'cache-control': "no-cache",
            'postman-token': "529a9a27-2e62-0d64-aea9-c938d33ec5fd"
        }

        conn.request("PUT", url, payload, headers)#使用指定的方法和url向服务器发送请求

        res = conn.getresponse()#返回一个 HTTPResponse 实例
        data = res.read().decode("utf-8")#读取内容

        data=json.loads(data)
        logging.warning(data)
        print(data)

        conn.close()
    except Exception as Error:
        logger.error(Error)
#处理电话号码
def phone(dict_c,phe):

    if phe.startswith('0'):
        if len(phe) == 11:
            dict_c['ChannelPhone'] = "+86 " + phe
        elif len(phe) == 12 and "-" in phe:
            dic = phe.split("-")
            dict_c['ChannelPhone'] = "+86 " + dic[0] + dic[1]
        elif len(phe) > 12:
            dict_c['Remarks'] = phe
    else:
        dict_c['Remarks']=phe
    return dict_c

#处理手机号
def mobile(dict_c,mbe):

    if len(mbe) == 11:
        dict_c['ChannelPhone'] = '+86 ' + mbe
    elif len(mbe) > 11:
        aa = '(13\d|14[5|7]|15\d|166|17[3|6|7]|18\d)\d{8}'
        dit = re.search(aa, mbe).group()
        dict_c['ChannelPhone'] = '+86 ' + dit
        dict_c['Remarks'] = mbe
    return dict_c

#执行查询更改操作
def data_query(data):
    red = data
    data_url = '/api/v1.0/one/dsl/query?dsl={"OrderInfo":{"fields":"id","cond":{"==":{"name":"' + red['code'] + '"}}}}'
    red_id = post_meiqia(data_url)
    logging.warning(red_id)
    print(red_id)
    if red_id:
        red_url = '/api/v1.0/one/OrderInfo/'+red_id[0]['id']
        reds = red.pop('code')
        red['version']=red_id[0]['version']
        put_meiqia(red,red_url)
def saleout_query(data):
    red = data
    data_url = '/api/v1.0/one/dsl/query?dsl={"OrderInfo":{"fields":["id","LogisticsNumber"],"cond":{"==":{"name":"' + red['code'] + '"}}}}'
    red_id = post_meiqia(data_url)
    logging.warning(red_id)
    print(red_id)
    if red_id:
        if red_id[0]['LogisticsNumber']:
            red['LogisticsNumber'] = red['LogisticsNumber']+ ";"+red_id[0]['LogisticsNumber']
        red_url = '/api/v1.0/one/OrderInfo/'+red_id[0]['id']
        reds = red.pop('code')
        red['version']=red_id[0]['version']
        put_meiqia(red,red_url)

def revise_data(re_data):

    revise_data = re_data
    revise_url = '/api/v1.0/one/dsl/query?dsl={"Tickets_ReturnGoods":{"fields":"id","cond":{"==":{"XSNumbers":"' + revise_data['code'] + '"}}}}'
    revise_id = post_meiqia(revise_url)
    if revise_id:
        rev_url = '/api/v1.0/one/Tickets_ReturnGoods/'+revise_id[0]['id']
        revise_data['version'] = revise_id[0]['version']
        put_meiqia(revise_data,rev_url)

#查询并返回省，市，区的id
def get_id(object_name,record):

    get_url = '/api/v1.0/one/dsl/query?dsl={"'+object_name+'":{"fields":"id","cond":{"==":{"name":"' + parse.quote(record) + '"}}}}'
    obj_id = post_meiqia(get_url)
    # print(obj_id)
    return obj_id

#  处理data_queue的数据
class ThreadData(threading.Thread):

    def __init__(self, data_queue):
        threading.Thread.__init__(self)
        self.data_queue = data_queue
        self.data = []

    def run(self):

        while True:
            # if self.data_queue.empty() == True:
            #     time.sleep(5)
            #     if self.data_queue.empty() == True:
            #         break
            data = self.data_queue.get()
            (key, value), = data.items()
            if value['errcode'] == '20006':
                continue
            # print(type(value['errcode']))
            logging.warning(value)
            print(value)

            if key == 'customer':# 购买渠道
                url = "/api/v1.0/one/Channel/"
                data = value['customer']
                list_c=[]
                for i in data:
                    dict_c={}
                    dict_c['name'] = i['name']  # 购买渠道名称
                    if 'address' in i:
                        dict_c['ChannelAddress']=i['address']#联系地址
                    if 'contact' in i:
                        dict_c['ChannelContact'] = i['contact']  # 联系人
                    #考虑手机号和电话的情况
                    if 'mobile' in i or 'phone' in i:
                        if 'mobile' in i and 'phone' in i:
                            if i['mobile'] and i['phone']:
                                if i['mobile'] == i['phone']:
                                    if len(i['mobile']) == 11:
                                        dict_c['ChannelPhone']="+86 "+i['mobile']
                                    elif len(i['mobile']) == 12 and "-" in i['mobile']:
                                        dic = i['phone'].split("-")
                                        dict_c['ChannelPhone'] = "+86 " + dic[0] + dic[1]
                                    elif len(i['mobile'])>11 and "-" not in i['mobile']:
                                        dict_c['Remarks']=i['mobile']

                                elif  i['mobile'] != i['phone']:
                                    if len(i['mobile'])==11:
                                        dict_c['ChannelPhone'] = "+86 " + i['mobile']
                                        dict_c['Remarks']=i['phone']
                                    elif len(i['mobile']) > 11:
                                        aa='(13\d|14[5|7]|15\d|166|17[3|6|7]|18\d)\d{8}'
                                        dit =re.search(aa, i['mobile']).group()
                                        dict_c['name']='+86 '+ dit
                                        dict_c['Remarks']=i['mobile']+i['phone']

                            elif i['phone'] and not i['mobile'] :
                                phone(dict_c,i['phone'])
                            elif i['mobile'] and not i['phone']:
                                mobile(dict_c, i['mobile'])

                        elif 'mobile' in i and 'phone' not in i:
                            if i['mobile']:
                                mobile(dict_c,i['mobile'])
                        elif 'mobile' not in i and 'phone' in i:
                            if i['phone']:
                                phone(dict_c, i['phone'])
                    list_c.append(dict_c)

                payload = {"objects": list_c}

                post_meiqia(url,payload)
            elif key == 'saleorderlist':  # 订单信息
                url = "/api/v1.0/one/OrderInfo/"
                data = value['saleorderlist']
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
                    if 'fhstatus' in i:  # 发货状态(0=未发货;1=部分发货;2=全部发货)
                        if i['fhstatus'] == "0":
                            dict_s['Fhstatus'] = "未发货"
                        elif i['fhstatus'] == "1":
                            dict_s['Fhstatus'] = "部分发货"
                        else:
                            dict_s['Fhstatus'] = "全部发货"
                    list_s.append(dict_s)
                payload = {"objects": list_s}
                post_meiqia(url,payload)

            elif key == 'inventory':# 库存货信息
                url = "/api/v1.0/one/Product/"
                data = value['inventory']
                # print(data)
                list_i = []
                for i in data:
                    dict_i = {}
                    if 'end_date' in i:
                        if i['end_date']:
                            continue
                    if 'self_define1' in i:
                        dict_i['self_define1'] = i['self_define1']
                    dict_i['ProductNumber'] = i['code']  # 产品编码
                    if 'fRetailPrice' in i :
                        dict_i['TaxUnitPrice'] = float(i['fRetailPrice'])#含税单价
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
                    dict_i['Imptaxrate'] = float(i['iimptaxrate'])/100  # 进项税率
                    dict_i['TaxRate'] = float(i['tax_rate'])/100  # 销售税率
                    if 'ref_sale_price' in i:
                        dict_i['Price']=float(i['ref_sale_price'])#单价
                    if 'bbarcode' in i:
                        dict_i['Bbarcode']=i['bbarcode']#条形码管理
                    if 'defwarehousename' in i:
                        dict_i['Defwarehousename']=i['defwarehousename']#默认仓库名称
                    if 'defwarehouse' in i:
                        dict_i['Defwarehouse']=i['defwarehouse']#默认仓库
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
                            dict_i['Partid']=i['entry'][0]['partid']

                    list_i.append(dict_i)
                payload = {"objects": list_i}
                print(payload)
                post_meiqia(url,payload)
                # time.sleep(1)
            elif key == 'person':  # 个人信息
                url = "/api/v1.0/one/Salesman/"
                data = value['person']
                # print(data)
                list_p = []
                for i in data:
                    dict_p={}
                    dict_p["name"]=i["name"]
                    dict_p["PersonnelNumber"]=i["code"]
                    dict_p["DepartmentName"]=i["cdept_name"]
                    dict_p["DepartmentCode"]=i["cdept_num"]
                    list_p.append(dict_p)
                payload = {"objects": list_p}
                post_meiqia(url,payload)
            elif key == 'eb_tradelist':
                data = value['eb_tradelist']
                # print(data)
                for i in data:
                    logging.warning(i)
                    list_e = {}
                    if 'cshipcode' not in i:
                        continue
                    if 'cshipcode' in i :
                        if i['cshipcode']:
                            if 'FHXS' in i['cshipcode']:
                                list_e['code'] = i['cshipcode'].split('H')[1]
                            elif 'XS' not in i['cshipcode'] and 'FH' in i['cshipcode'] :
                                list_e['code'] = 'XS'+ i['cshipcode'].split('H')[1]
                            else :
                                list_e['code'] = i['cshipcode']
                        else:
                            continue
                    if 'receiver_name' in i:
                        list_e['ConsigneeNam'] = i['receiver_name']
                    if 'receiver_state' in i:
                        if len(i['receiver_state']) == 2:
                            if i['receiver_state'] in ['北京','天津','上海','重庆']:
                                state_id = get_id("Province", i['receiver_state'] + '市')
                                if state_id:
                                    list_e['Cprovince'] = state_id[0]['id']
                            else:
                                state_id = get_id("Province", i['receiver_state'] + '省')
                                if state_id:
                                    list_e['Cprovince'] = state_id[0]['id']
                        else:
                            state_id = get_id("Province",i['receiver_state'])
                            if state_id:
                                list_e['Cprovince'] = state_id[0]['id']
                    if 'receiver_city' in i:

                        if "市" in i['receiver_city']:
                            city_id = get_id("Municipality",i['receiver_city'])
                            if city_id:
                                list_e['Scity'] = city_id[0]['id']

                        else :
                            city_id = get_id("Municipality", i['receiver_city'] + '市')
                            if city_id:
                                list_e['Scity'] = city_id[0]['id']

                    if 'receiver_district' in i:
                        dis_id = get_id("Prefecture",i['receiver_district'])
                        if dis_id:
                            list_e['Cdistrict'] = dis_id[0]['id']
                    if 'receiver_address' in i:
                        list_e['Address'] = i['receiver_address']
                    if 'receiver_mobile' in i:
                        if 7<= len(i['receiver_mobile'])<=11:
                            if Phone().find(i['receiver_mobile']):
                                list_e['Phone'] = "+86 "+ i['receiver_mobile']
                            else:
                                list_e['Remarks'] = "电话号码:" + i['receiver_mobile']
                        else:
                            list_e['Remarks']= "电话号码:" + i['receiver_mobile']
                    logging.warning(list_e)
                    print(list_e)
                    if list_e['code']:
                        data_query(list_e)
            elif key == 'saleoutlistall':
                data = value['saleoutlistall']
                for i in data:
                    list_s = {}
                    list_a = {}
                    if 'subordercode' not in i :
                        continue
                    if 'subordercode' in i:
                        if i['subordercode']:
                            list_s['code'] = i['subordercode']

                    # if 'quantity' in i:
                    #     if float(i['quantity']) <= 0:
                    #         list_a['code']=i['subordercode']
                    #         list_a['IsNotEntrepot'] = True
                            # revise_data(list_a)
                    list_s['LogisticsNumber'] = i['subconsignmentcode']
                    saleout_query(list_s)

            self.data_queue.task_done()
# 定时执行获取token
def runTask(day=0, hour=0, min=0, second=0):
    # Init time
    now = datetime.datetime.now()#返回一个当前的时间
    strnow = now.strftime('%Y-%m-%d %H:%M:%S')

    # First next run time
    period = datetime.timedelta(days=day, hours=hour, minutes=min, seconds=second)
    next_time = now + period
    strnext_time = next_time.strftime('%Y-%m-%d %H:%M:%S')

    while True:

        iter_now = datetime.datetime.now()
        iter_now_time = iter_now.strftime('%Y-%m-%d %H:%M:%S')
        if str(iter_now_time) == str(strnext_time):
            new_token = Toekn().run()
            global token
            token = new_token
            iter_time = iter_now + period
            strnext_time = iter_time.strftime('%Y-%m-%d %H:%M:%S')
            continue

        time.sleep(10)
        if data_queue.empty():
            break

#执行程序
def main():
    page_index = '1'
    end_url = 'from_account=bolebaokaifa&to_account=bolebao&app_key=opa87ad77a2a44f12df&token=' + \
        token + '&page_index=' + page_index + '&rows_per_page=20&ds_sequence=1'
    start_date = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    end_date = (datetime.date.today()).strftime("%Y-%m-%d ")

    # 销售订单信息
    order_url = 'https://api.yonyouup.com/api/saleorderlist/batch_get?' + end_url
    #业务员信息
    person = 'https://api.yonyouup.com/api/person/batch_get?' + end_url
    # 客户信息
    customer = 'https://api.yonyouup.com/api/customer/batch_get?' + end_url
    #产品档案
    inventory = 'https://api.yonyouup.com/api/inventory/batch_get?' + end_url
    #电商订单
    eb_tradelist = 'https://api.yonyouup.com/api/eb_tradelist/batch_get?' + end_url
    #出库单
    saleoutlistall = "https://api.yonyouup.com/api/saleoutlistall/batch_get?" + end_url

    list = [person]

    for i in list:
        url_queue.put(i)

    for i in range(2):
        try:
            logger.info('开启多线程执行请求任务')
            t = ThreadYongYou(url_queue)
            t.setDaemon(True)
            t.start()

        except Exception as error:
            logger.error('开启请求线程异常')
            print(error)

    for i in range(1):
        try:
            logger.info('开启线程获取queue数据')
            t = ThreadData(data_queue)
            t.setDaemon(True)
            t.start()
        except Exception as error:
            logger.error('开启线程请求queue异常')
            print(error)

    tok = threading.Thread(runTask(day=0, hour=1, min=30))
    tok.start()
    tok.join()

    time.sleep(4)

    url_queue.join()
    data_queue.join()

    if data_queue.empty():
        # print(data_queue.empty())
        tok.join()


if __name__ == '__main__':

        main()
