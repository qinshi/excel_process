# -*- coding: utf8 -*-

import xlrd


class ExcelProcessor(object):
    @classmethod
    def do_process(cls, file_name):
        workbook = xlrd.open_workbook(file_name)

        sheet_names = workbook.sheet_names()

        for sheet_name in sheet_names:
            sheet2 = workbook.sheet_by_name(sheet_name)
            print sheet_name
            rows = sheet2.row_values(1) # 获取第四行内容
            cols = sheet2.col_values(1) # 获取第二列内容
            print rows
            print cols
