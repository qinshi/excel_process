# -*- coding: utf8 -*-
import xlrd
from excel_processor import ExcelProcessor


def get_names():
    return [u'/Users/sq/work/excel_process/src/src2.xls']


file_names = get_names()
for file_name in file_names:
    ExcelProcessor.do_process(file_name)


