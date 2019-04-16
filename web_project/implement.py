# -*- coding:utf-8 -*-
import os
import sys

from webs_product import product_main
from webs_person import person_main
from webs_channel import channel_main
from webs_receipt import receipt_main
from webs_invoice import invoice_main
from webs_orderinfo import orderinfo_main
from webs_sn import sn_main



def main():

    # os.system('python ./web_person.py')
    # # os.system('python ./web_channel.py')
    # # os.system('python ./web_product.py')
    # # os.system('python ./web_orderinfo.py')
    # # os.system('python ./web_receipt.py')
    # # os.system('python ./web_invoice.py')
    # # os.system('python ./web_sn.py')
    # product_main()
    person_main()
    # channel_main()
    # orderinfo_main()
    # receipt_main()
    # invoice_main()
    # sn_main()

if __name__ == '__main__':

    if len(sys.argv) != 2:

        print('输入格式错误，格式为: python manage.py config路径')

    else:

        if sys.argv[1] in ['./config/formal.ini','./config/testing.ini']:

            with open(sys.argv[1],'r') as file:
                cfg = file.read()
            with open('./config/config.ini','w') as content:
                content.write(cfg)

            main()

        else:
            print('输入的config路径错误')
