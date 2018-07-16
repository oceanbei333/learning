# -*- coding: utf-8 -*-
import pandas as pd
from copy import deepcopy
import jieba
import re
ori_xls_file = u'/Users/isea/Documents/ipm/ipm项目名单.xlsx'
xls_files = [
    u'/Users/isea/Documents/ipm/PMS表单汇总/浦东交投二级表单.xlsx',
    #u'/Users/isea/Documents/ipm/PMS表单汇总/古镇公司一级表单.xlsx',
    u'/Users/isea/Documents/ipm/PMS表单汇总/轨交投资一级表单.xlsx',
    u'/Users/isea/Documents/ipm/PMS表单汇总/浦东地产二级表单.xlsx',
    u'/Users/isea/Documents/ipm/PMS表单汇总/浦东地产一级表单.xlsx',
    u'/Users/isea/Documents/ipm/PMS表单汇总/浦东新城镇一级表单.xlsx',
]


def function_filter(pat):
    def sub_func(data_1):
        try:
            return re.findall(pat, data_1)
        except:
            return data_1 == pat

    return sub_func


def function_filter_all(pat):
    def sub_func(data_1):
        return data_1 == pat

    return sub_func


def get_search_domains(name):
    '''
        根据正则匹配关键字
    '''

    pat_list = [
        '\D(\S{2}-\d{2})',
        '(\S{2})单元',
        '(\S{2})停车',
        '(\S{2})工程',
        '(\S期)',
        '(\S{2})站',
        '(\S{2})路',
        '(\S{2})段',
        '(\S{2})镇',
        '(\S{2})项目',
        '(\S{2})号线',
        '(\S{2})园',
        '(\S{2})区',
        '(\S{2})村',
    ]
    pat = '|'.join(pat_list)
    keys = re.findall(pat, name)
    key_list = []
    for i in keys:
        for j in i:
            if j:
                key_list.append(j)
    return key_list


def get_search_domains_jieba(name, cut_all=False):
    seg_list = jieba.cut(name, cut_all)
    return seg_list


data_result = {}
found_list = []
excel_list = []
ori_data = pd.read_excel(ori_xls_file, 'Sheet1')
ori_data_name = list(ori_data['项目名称'])


def filter_data(xls_file):
    data = pd.read_excel(xls_file, 'Sheet1')
    data_name = list(data['项目名称'])
    excel_list.extend(data_name)

    # 根据项目名称精确匹配
    print(xls_file)
    for name in data_name:
        if name != name:
            continue
        data_result[name] = []
        data_filter = ori_data_name
        data_filter_all = list(filter(function_filter_all(name), data_filter))
        if data_filter_all:
            ori_data_name.remove(name)
            data_result[name].append(name)
            found_list.append(name)
    # 根据XX路、XX号线、XX地块匹配
    for name in data_name:
        if name != name:
            continue
        data_filter = ori_data_name
        key_list = get_search_domains(name)
        if not key_list:
            continue
        for j in list(key_list):
            print(j)
            data_filter_temp = list(filter(function_filter(j), data_filter))
            if len(data_filter_temp) == 1:
                data_filter = data_filter_temp
                break
        if len(data_filter) > 1:
            for j in key_list:
                data_filter_temp = list(
                    filter(function_filter(j), data_filter))
                if len(data_filter_temp) == 0:
                    continue
                else:
                    data_filter = data_filter_temp

        print(len(data_filter))
        if 0 < len(data_filter) < 5:
            for data_a in data_filter:
                ori_data_name.remove(data_a)
                data_result[name].append(data_a)
                found_list.append(name)
    print(len(found_list))


not_found_list = []
for xls_file in xls_files:
    filter_data(xls_file)

data_result
for name in excel_list:
    if name not in found_list:
        not_found_list.append(name)


def convert_to_excel(data):
    array_data = []
    for key, values in data.items():
        if not values:
            array_data.append([key, '', ''])
        for value in values:
            project_number = ori_data[ori_data['项目名称'] == value][
                '项目编号'].values[0]
            array_data.append([key, value, project_number])
    n = len(array_data)
    pd_var = pd.DataFrame(array_data, index=range(n), columns=list('ABC'))
    pd_var.to_excel('execl和系统匹配的项目.xlsx', sheet_name='Sheet1')


def convert_to_excel2(data, name):
    array_data = []
    for value in data:
        if not value or value != value:
            continue
        array_data.append([value])
    n = len(array_data)
    pd_var = pd.DataFrame(array_data, index=range(n), columns=list('A'))
    pd_var.to_excel(name, sheet_name='Sheet1')


convert_to_excel2(not_found_list, 'excel中未被匹配项目.xlsx')
convert_to_excel2(ori_data_name, '系统中未被匹配项目.xlsx')
convert_to_excel(data_result)
