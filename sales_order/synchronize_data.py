# -*- coding:utf-8 -*-

import xlrd

from common_method import loger,Methods,group_data
from consultative_order import analysis_consultative
from insert_order import analysis_insert
from complaint_order import analysis_complaint
from dismantling_order import analysis_dismantling

def analysis_file(file_name):

    book = xlrd.open_workbook(file_name)
    url = 'https://crm.meiqia.com/api/v1.0/one/'
    sheet_name = ["咨询工单","安装工单","投诉工单","拆机工单"]
    for sheet in sheet_name:
        # print(sheet)
        read_sheet = book.sheet_by_name(sheet)
        if sheet == "咨询工单":
            consultative_list = analysis_consultative(read_sheet)
            consultative_group = group_data(consultative_list)
            for consultative in consultative_group:
                Methods(url+'Tickets_Consultation/',{'objects':consultative}).post_data()
        elif sheet == "安装工单":
            insert_list = analysis_insert(read_sheet)
            for insert in insert_list:
                insert_url = url+'Tickets_Install/'
                if 'service' in insert:
                    service = insert.pop('service')
                    insert_id = Methods(insert_url,{'objects':[insert]}).post_data()
                    if insert_id:
                        service['Tickets_InstallID'] = insert_id
                        Methods(url+'ServiceInformation',{'objects':[service]}).post_data()
                else:
                    Methods(insert_url,{'objects':[insert]}).post_data()

        elif sheet == "投诉工单":

            complint_list = analysis_complaint(read_sheet)
            complint_group = group_data(complint_list)
            for complint in complint_group:
                Methods(url+'Tickets_Complaint/',{'objects':complint}).post_data()

        elif sheet == "拆机工单":
            dismantling_list = analysis_dismantling(read_sheet)
            for dismantling in dismantling_list:
                dismantling_url = url + 'Tickets_Dismantling/'
                if 'service' in dismantling and 'visit' in dismantling:
                    dismantling_service = dismantling.pop('service')
                    dismantling_visit = dismantling.pop('visit')
                    dismantling_id = Methods(dismantling_url,{'objects':[dismantling]}).post_data()
                    if dismantling_id:
                        dismantling_service['Tickets_DismantlingID'] = dismantling_id
                        dismantling_visit['Tickets_DismantlingID'] = dismantling_id
                        Methods(url+'ServiceInformation',{'objects':[dismantling_service]}).post_data()
                        Methods(url+'TicketsVisit_Dismantling',{'objects':[dismantling_visit]}).post_data()

                elif 'service' in dismantling and 'visit' not in dismantling:
                    dismantling_service = dismantling.pop('service')

                    dismantling_id = Methods(dismantling_url,{'objects':[dismantling]}).post_data()
                    if dismantling_id:
                        dismantling_service['Tickets_DismantlingID'] = dismantling_id

                        Methods(url+'ServiceInformation',{'objects':[dismantling_service]}).post_data()
                elif 'service' not in dismantling and 'visit' in dismantling:

                    dismantling_visit = dismantling.pop('visit')
                    dismantling_id = Methods(dismantling_url,{'objects':[dismantling]}).post_data()
                    if dismantling_id:

                        dismantling_visit['Tickets_DismantlingID'] = dismantling_id

                        Methods(url+'TicketsVisit_Dismantling',{'objects':[dismantling_visit]}).post_data()
                else:
                    Methods(dismantling_url, {'objects': [dismantling]}).post_data()


if __name__ == '__main__':
    analysis_file('1-201601-20161130.xlsx')











