# -*- coding:utf-8 -*-

from suds import Client

from public_methods import loger

class Web_interface:

    def __init__(self,condition):

        self.url = 'http://124.207.40.126:9000/BLBWEB/WebService.asmx?WSDL'
        self.key = 'key01'
        self.condition = condition

    def obtain_data(self):

        try:
            client = Client(self.url)
            return client
        except Exception as error:
            loger().info("连接webservice方法时报错，报错信息:%s" %error)
            return None

    def person_info(self):#业务员信息

        try:
            person = self.obtain_data()
            if person:
                person_data = person.service.Person(self.key,self.condition)
                if person_data:
                    return person_data
                else:
                    return None
            else:
                return None
        except Exception as error:

            loger().info("调用获取业务员信息方法时报错，报错信息:%s" %error)
            return None

    def customer_info(self):#购买渠道

        try:
            customer = self.obtain_data()
            if customer:
                customer_data = customer.service.Cus(self.key,self.condition)
                if customer_data:
                    return customer_data
                else:
                    return None
            else:
                return None
        except Exception as error:

            loger().info("调用获取购买渠道方法时报错，报错信息:%s" % error)
            return None

    def product_info(self):#产品档案

        try:
            product = self.obtain_data()
            if  product:
                product_data = product.service.Inv(self.key,self.condition)
                if product_data:
                    return product_data
                else:
                    return None
            else:
                return None
        except Exception as error:

            loger().info("调用获取产品档案方法时报错，报错信息:%s" % error)
            return None

    def order_info(self):#XS订单

        try:
            order = self.obtain_data()
            if order:
                order_data = order.service.SaOrder(self.key,self.condition)
                if order_data:
                    return order_data
                else:
                    return None
            else:
                return None
        except Exception as error:

            loger().info("调用获取XS订单方法时报错，报错信息:%s" % error)
            return None

    def sales_shipment(self):#发货单

        try:
            shipment = self.obtain_data()
            if shipment:
                shipment_data = shipment.service.SaFhd(self.key,self.condition)
                if shipment_data:
                    return shipment_data
                else:
                    return None
            else:
                return None
        except Exception as error:

            loger().info("调用获取发货单方法时报错，报错信息:%s" % error)
            return None

    def sales_outlet(self):#出库单

        try:
            outlet = self.obtain_data()
            if outlet:
                outlet_data = outlet.service.SaRd32(self.key,self.condition)
                if outlet_data:
                    return outlet_data
                else:
                    return None
            else:
                return None
        except Exception as error:

            loger().info("调用获取出库单方法时报错，报错信息:%s" % error)
            return None

    def web_ordercount(self):#订单数量

        try:
            order_count = self.obtain_data()
            if order_count:
                ordercount_data = order_count.service.SaOrderCount(self.key,self.condition)
                if ordercount_data:
                    return ordercount_data
                else:
                    return None
            else:
                return None
        except Exception as error:

            loger().info("调用获取订单数量方法时报错，报错信息:%s" % error)
            return None

    def web_shipmentcount(self):#发货单数量

        try:
            shipment_count = self.obtain_data()
            if shipment_count:
                shipmentcount_data = shipment_count.service.SaFhdCount(self.key,self.condition)
                if shipmentcount_data:
                    return shipmentcount_data
                else:
                    return None
            else:
                return None
        except Exception as error:

            loger().info("调用获取发货单数量方法时报错，报错信息:%s" % error)
            return None

    def web_outletcount(self):#出库单数量

        try:
            outlet_count = self.obtain_data()
            if outlet_count:
                outletcount_data = outlet_count.service.SaRd32Count(self.key,self.condition)
                if outletcount_data:
                    return outletcount_data
                else:
                    return None
            else:
                return None
        except Exception as error:

            loger().info("调用获取出库单数量方法时报错，报错信息:%s" % error)
            return None