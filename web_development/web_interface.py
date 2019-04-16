# -*- coding:utf-8 -*-
from suds import Client

from logger import loger

class Web_interface:

    def __init__(self,order_strwhere = None):

        self.url = 'http://u8.bolebao.com:9000/BLBWEB/WebService.asmx?WSDL'
        self.strwhere = ''
        self.key = 'key01'
        self.order = order_strwhere

    def obtain_data(self):#连接webservice

        try:
            client = Client(self.url)
            return client
        except Exception as error:
            loger().error(error)
            return None

    def person_info(self):#业务员

        person = self.obtain_data()
        if person:
            person_data = person.service.Person(self.key,self.strwhere)
            if person_data:
                return person_data
            else:
                return None
        else:
            return None

    def customer_info(self):#客户档案

        customer = self.obtain_data()
        if customer:
            customer_data = customer.service.Cus(self.key,self.strwhere)
            if customer_data:
                return customer_data
            else:
                return None
        else:
            return None

    def product_info(self):#存货档案

        product = self.obtain_data()
        if product:
            product_data = product.service.Inv(self.key,self.strwhere)
            if product_data:
                return product_data
            else:
                return None
        else:
            return None

    def order_info(self):#销售订单

        order = self.obtain_data()
        order_data = order.service.SaOrder(self.key,self.order)
        return order_data

    def sales_shipment(self):#发货单

        shipment = self.obtain_data()
        if shipment:
            shipment_data = shipment.service.SaFhd(self.key,self.order)
            if shipment_data:
                return shipment_data
            else:
                return None
        else:
            return None

    def sales_outlet(self):#出库单

        outlet = self.obtain_data()
        if outlet:
            outlet_data = outlet.service.SaRd32(self.key,self.order)
            if outlet_data:
                return outlet_data
            else:
                return None
        else:
            return None

    def sales_mix(self):

        mix = self.obtain_data()
        mix_data = mix.service.SaTj(self.key,self.strwhere)
        return mix_data
