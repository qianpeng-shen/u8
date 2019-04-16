# encoding=utf-8
import re

from urllib import parse
from logger import post_meiqia,put_meiqia




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
            aa = '(13\d|14[5|7]|15\d|166|17[3|6|7]|18\d)\d{8}'
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