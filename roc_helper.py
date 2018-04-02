# -*- coding: utf8 -*-


class DataItem(object):
    def __init__(self):
        self.name = None
        self.data_detals = []


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
        # TODO: do roc calculate
        self.roc_pool[self.__get_roc_id(src_item.name, target_item.name)] = roc
        return roc

    def get_roc_value(self, src_name, target_name, cutoff, type):
        return 0

    def __get_roc_id(self, src_name, target_name):
        return src_name + '_' + target_name
