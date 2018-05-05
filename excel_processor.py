# -*- coding: utf8 -*-

import xlrd
from roc_helper import RocHelper, DataItem


class ExcelProcessor(object):
    @classmethod
    def do_process(cls, file_name, target_col):

        print 'enter do process...'

        target_col = target_col.decode('utf-8')
        data = cls.get_data(file_name)

        print 'after get data...'

        titles = data.row_values(1)
        try:
            target_index = titles.index(target_col)
        except Exception as e:
            print '不存在列：' + target_col
            return

        cal_title_ids = cls.get_cal_title_ids(data, titles)
        target_data_item = DataItem(titles[target_index], data.col_values(target_index)[2:])
        roc_helper = RocHelper()
        for cal_title_id in cal_title_ids:
            cal_data_item = DataItem(titles[cal_title_id], data.col_values(cal_title_id)[2:])
            try:
                roc_helper.add_roc(src_item=cal_data_item, target_item=target_data_item)
            except Exception as e:
                print 'add roc fail, e = ' + repr(e)

        print 'after calculate roc...'

        roc_pool = roc_helper.roc_pool
        choose_keys = []
        for key in roc_pool.keys():
            if roc_pool[key].auc > 0.9:
                choose_keys.append(key)

        pt = 0.05

        row_num = len(data.col_values(1))
        lrs = {}

        for row_idx in xrange(2, row_num):
            try:
                row_lrs = {}
                for choose_key in choose_keys:
                    column_title = roc_pool[choose_key].item_name
                    column_index = titles.index(column_title)
                    column_value = data.col_values(column_index)[row_idx]
                    item = roc_pool[choose_key].item_detail[column_value]
                    temp_lr = item['tpr'] / item['fpr']
                    row_lrs[column_title] = temp_lr

                lrs[row_idx] = row_lrs
            except Exception as e:
                print 'cal row ' + str(row_idx) + ' fail...'

        valid_target_data = []
        valid_src_data = []

        print 'before cal p...'

        for key in lrs.keys():
            row_lr = lrs[key]
            total_lr = 1
            for item in row_lr:
                total_lr = total_lr * row_lr[item]

            temp_p = 1 - (1 - pt) / (1 - pt + pt * total_lr)

            valid_target_data.append(data.col_values(target_index)[key])
            valid_src_data.append(temp_p)

        print 'after cal p...'

        valid_target_data_item = DataItem(titles[target_index], valid_target_data)
        valid_src_data_item = DataItem('final_p', valid_src_data)
        valid_roc_helper = RocHelper()

        valid_roc = valid_roc_helper.add_roc(src_item=valid_src_data_item, target_item=valid_target_data_item)
        temp_p = 0
        temp_max = 0
        for item in valid_roc.item_detail:
            if valid_roc.item_detail[item]['tpr'] + (1 - valid_roc.item_detail[item]['fpr']) > temp_max:
                temp_max = valid_roc.item_detail[item]['tpr'] + (1 - valid_roc.item_detail[item]['fpr'])
                temp_p = item

        print '=================='
        print temp_max
        print temp_p


    @classmethod
    def get_data(cls, file_name):
        workbook = xlrd.open_workbook(file_name)
        sheet_names = workbook.sheet_names()
        sheet_name = sheet_names[0]
        data = workbook.sheet_by_name(sheet_name)
        return data

    @classmethod
    def get_cal_title_ids(cls, data, titles):
        start = False
        cal_titles_ids = []
        for i in range(len(titles)):
            values = data.col_values(i)
            if titles[i] == 'WBC(10^3/uL)':
                start = True

            if not start:
                continue

            if titles[i].endswith('/M'):
                continue

            for j in range(1, 10):
                if values[j]:
                    cal_titles_ids.append(i)
                    break

        return cal_titles_ids

    @classmethod
    def get_need_cal_columns(cls, workbook):
        return []
