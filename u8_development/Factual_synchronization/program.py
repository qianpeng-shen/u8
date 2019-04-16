# encoding=utf-8
import re

from urllib import parse

from logger import post_meiqia,put_meiqia,del_meiqia

#查询后执行更改或者新增数据
def data_query(data, data_name, url, alias):
    red = data
    data_url = '/api/v1.0/one/dsl/query?dsl={"' + data_name + '":{"fileds":"id","cond":{"==":{"'+ alias +'":"' + red[
        alias] + '"}}}}'
    red_id = post_meiqia(data_url)
    # print(red_id)
    if red_id:
        red_url = '/api/v1.0/one/' + data_name + '/' + red_id[0]['id']
        # print(red_url)
        reds = red.pop(alias)
        red['version'] = red_id[0]['version']
        put_meiqia(red, red_url)
    else:
        url = url
        post_meiqia(url,{"objects": [data]})


class Person():
    def __init__(self,data):
        self.data = data
    def get_id(self):

        data_url = '/api/v1.0/one/dsl/query?dsl={"Salesman":{"fileds":"id","cond":{"==":{"PersonnelNumber":"' + self.data['PersonnelNumber'] + '"}}}}'
        person_id = post_meiqia(data_url)
        return person_id

    def incumbency(self):

        red_id = self.get_id()
        if red_id:
            red_url = '/api/v1.0/one/Salesman/' + red_id[0]['id']
            reds = self.data.pop('PersonnelNumber')
            self.data['version'] = red_id[0]['version']
            put_meiqia(self.data, red_url)
        else:
            url =  "/api/v1.0/one/Salesman/"
            post_meiqia(url, {"objects": [self.data]})

    def retreat(self):

        red_id = self.get_id()
        # print(red_id)
        if red_id:
            # print(red_id['id'])
            red_url = '/api/v1.0/one/Salesman/'+ red_id['id'] +'/?version='+str(red_id[0]['version'])
            del_meiqia(red_url)


#处理电话号码和手机号码，获取省市区的id
class Handle():
    def __init__(self,record,target):

        self.record = record
        self.target = target

    def get_id(self):

        get_url = '/api/v1.0/one/dsl/query?dsl={"' + self.target + '":{"fileds":"id","cond":{"==":{"name":"' + parse.quote(self.record) + '"}}}}'
        obj_id = post_meiqia(get_url)
        return obj_id

    def get_mobile(self):

        if len(self.target) == 11:
            self.record['ChannelPhone'] = '+86 ' + self.target
        elif len(self.target) > 11:
            aa = '^((13[0-9])|(14[5,7])|(15[0-3,5-9])|(17[0,3,5-8])|(18[0-9])|166|198|199|(147))\\d{8}$'
            dit = re.search(aa, self.target).group()
            self.record['ChannelPhone'] = '+86 ' + dit
            self.record['Remarks'] = self.target
        return self.record

    def get_phone(self):

        if self.target.startswith('0'):
            if len(self.target) == 11:
                self.record['ChannelPhone'] = "+86 " + self.target
            elif len(self.target) == 12 and "-" in self.target:
                dic = self.target.split("-")
                self.record['ChannelPhone'] = "+86 " + dic[0] + dic[1]
            elif len(self.target) > 12:
                self.record['Remarks'] = self.target
        else:
            self.record['Remarks'] = self.target
        return self.record

#用于处理电商订单和出库单数据 查询和执行
class Saleout_eb():
    def __init__(self,data):

        self.data = data

    def saleout_query(self):

        data_url = '/api/v1.0/one/dsl/query?dsl={"OrderInfo":{"fields":["id","LogisticsNumber"],"cond":{"==":{"name":"' + self.data + '"}}}}'
        red_id = post_meiqia(data_url)
        if red_id:
            return red_id[0]
        else:
            return None

    def eb_query(self):

        data_url = '/api/v1.0/one/dsl/query?dsl={"OrderInfo":{"fields":"id","cond":{"==":{"name":"' + self.data + '"}}}}'
        red_id = post_meiqia(data_url)
        if red_id:
            return red_id[0]
        else:
            return None

    def execution(self):

        red_url = '/api/v1.0/one/OrderInfo/'+self.data['code']
        reds = self.data.pop('code')
        put_meiqia(self.data,red_url)