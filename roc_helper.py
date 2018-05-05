# -*- coding: utf8 -*-

import pdb
import numpy as np
from sklearn import metrics

class DataItem(object):
    def __init__(self, name, data_details):
        self.name = name
        self.data_details = data_details


class RocItem(object):
    def __init__(self):
        self.item_name = None
        self.target_name = None
        self.auc = 0
        self.item_detail = {}


class RocHelper(object):
    def __init__(self):
        self.roc_pool = {}

    def add_roc(self, src_item, target_item):
        roc = RocItem()
        raw_y = []
        raw_pred = []
        for index in range(len(src_item.data_details)):
            try:
                temp_raw_pred = float(src_item.data_details[index])
                raw_pred.append(temp_raw_pred)
                if target_item.data_details[index] != u'':
                    raw_y.append(1)
                else:
                    raw_y.append(0)
            except Exception as e:
                print repr(e)

        y = np.array(raw_y)
        pred = np.array(raw_pred)
        fpr, tpr, thresholds = metrics.roc_curve(y, pred, pos_label=1)
        auc = metrics.auc(fpr, tpr)

        roc.target_name = target_item.name
        roc.item_name = src_item.name
        roc.auc = auc
        for index in range(len(thresholds)):
            roc.item_detail[thresholds[index]] = {'tpr': tpr[index],
                                                  'fpr': fpr[index]}

        self.roc_pool[self.__get_roc_id(src_item.name, target_item.name)] = roc
        return roc

    def get_roc_value(self, src_name, target_name, cutoff, type):
        return 0

    def __get_roc_id(self, src_name, target_name):
        return src_name + '_' + target_name
