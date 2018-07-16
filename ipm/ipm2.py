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
xls_file = u'/Users/isea/Documents/ipm/PMS表单汇总/浦东新城镇一级表单.xlsx'

# 读取数据
same = []
no_same = []
project_ids = []
list_project = []
data = xlrd.open_workbook(xls_file)
for table in data.sheets():
    nrows = table.nrows
    for i in range(nrows):
        j = i + 3
        if j < nrows:
            # 项目编号精确匹配
            name = table.row(j)[0].value
            infos = re.findall(
                r'(\S{2}路)|(\S\S号线)|(\S\S站)|(\S\S\S\S\S地块)', name.encode('utf-8'))
            for i in infos:
                for j in i:
                    print(j)
                    j.decode('utf-8')