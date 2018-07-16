# -*- coding: utf-8 -*-
import openerplib
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import xlrd
import xmlrpclib
from os import path
from optparse import OptionParser
import re
import pandas

h = '10.100.1.168'
db = 'pms_db'
u = 'admin'
pw = 'Password01!'

connection = openerplib.get_connection(
    hostname=h, database=db, login=u, password=pw)
project_model = connection.get_model('yins.ipm.project')

# xls_file = u'/Users/zhaoshuzhen/dev/ipm/tools/ini_data/ini_project/浦东交投二级表单.xlsx'
# xls_file = u'/Users/zhaoshuzhen/dev/ipm/tools/ini_data/ini_project/古镇公司一级表单.xlsx'
# xls_file = u'/Users/zhaoshuzhen/dev/ipm/tools/ini_data/ini_project/轨交投资一级表单.xlsx'
# xls_file = u'/Users/zhaoshuzhen/dev/ipm/tools/ini_data/ini_project/浦东地产二级表单.xlsx'
# xls_file = u'/Users/zhaoshuzhen/dev/ipm/tools/ini_data/ini_project/浦东地产一级表单.xlsx'
xls_file = u'/Users/isea/Documents/ipm/PMS表单汇总/浦东新城镇一级表单.xlsx'
ori_xls_file = u'/Users/isea/Documents/ipm/ipm项目名单.xlsx'

# 读取数据
same = []
no_same = []
project_ids = []
list_project = []
project_ids_by_name = project_model.search([])
data = xlrd.open_workbook(xls_file)
for table in data.sheets():
    nrows = table.nrows
    for i in range(nrows):
        j = i + 3
        if j < nrows:
            # 项目编号精确匹配
            if table.row(j)[1].value:
                project_id = project_model.search([
                    ('project_number', '=', table.row(j)[1].value)])
                if project_id:
                    same.append(j)
                    project_ids.append(j)
                    print(table.row(j)[0].value)
                else:
                    no_same.append(j)
            # 名字精确匹配
            name = table.row(j)[0].value
            project_id = project_model.search([
                ('name', '=', name), 
                ('id', 'not in', project_ids)])
            if project_id:
                if project_id not in same:
                    same.append(j)
                    print(table.row(j)[0].value)
                    if project_id in no_same:
                        no_same.remove(j)
            else:
                if j not in no_same:
                    no_same.append(j)
            # 名字模糊匹配
            print(name)
            infos = re.findall(
                r'(\S\S路)|(\S\S号线)|(\S\S站)|(\S\S\S\S\S地块)', name.encode('utf-8'))
            print(infos)
            if infos:
                domain = [('id', 'not in', project_ids)]
                for info in infos:
                    for info_a in info:
                        if info:
                            domain.append(('name', 'like', info_a))
                            break
                    break
                print(domain)
                project_id = project_model.search(domain)
                if project_id:
                    if project_id not in same:
                        same.append(j)
                        print(table.row(j)[0].value)
                        if project_id in no_same:
                            no_same.remove(j)


print('都有'+str(same))
print('excel有，系统里没有'+ str(no_same))