from utils import *
import os
from collections import Counter
from loguru import logger


class RecordItem:
    def __init__(self, text):
        self.record_dict = {}
        lines = text.split('\n')
        blocks = []
        for line in lines:
            if line[:4].replace(' ', '') != '':
                blocks.append([line])
            else:
                blocks[-1].append(line)
        for block in blocks:
            prefix = block[0][:4].replace(" ", "")
            content = ''
            for line in block:
                content += line[6:]
            if prefix not in self.record_dict.keys():
                self.record_dict[prefix] = [content]
            else:
                self.record_dict[prefix] = self.record_dict[prefix] + [content]

    def __getitem__(self, item):
        try:
            return self.record_dict[item]
        except KeyError:
            # logger.warning('There is no item {} in object {}'.format(item, self.record_dict['PMID'][0]))
            pass

    def __setitem__(self, key, value):
        self.record_dict[key] = value

    def __repr__(self):
        return str(self.record_dict['PMID'][0])


class Parser:
    def __init__(self, file_paths):
        self.record_items = []
        for file_path in file_paths:
            with open(file_path, mode='r', encoding='utf-8') as file:
                origin_data = file.read()
                records = origin_data.split('\n\n')
                for record in records:
                    self.record_items.append(RecordItem(record))

    @staticmethod
    def cluster_by_year(record_items):
        cluster_years = {}
        for item in record_items:
            if item['DP'][0][:4] in cluster_years.keys():
                cluster_years[item['DP'][0][:4]].append(item)
            else:
                cluster_years[item['DP'][0][:4]] = [item]
        return cluster_years

    @staticmethod
    def filter_chinese(record_items, first_author: bool = True):
        chinese_items = []
        for item in record_items:
            try:
                if first_author:
                    if string_search('China', item['AD'][0]):
                        chinese_items.append(item)
                else:
                    if string_search('China', item['AD']):
                        chinese_items.append(item)
            except TypeError:
                continue
        return chinese_items

    @staticmethod
    def cluster_by_journal(record_items):
        cluster_journals = {}
        for item in record_items:
            if item['JT'][0].strip() in cluster_journals.keys():
                cluster_journals[item['JT'][0].strip()].append(item)
            else:
                cluster_journals[item['JT'][0].strip()] = [item]
        return cluster_journals

    @staticmethod
    def statistic_meshes(record_items):
        all_meshes = []
        for item in record_items:
            try:
                all_meshes += item['MH']
            except TypeError:
                continue
        return Counter(all_meshes)

    @staticmethod
    def filter_mesh(record_items, keywords):
        filtered_items = []
        for item in record_items:
            try:
                if strings_search(keywords, item['MH']):
                    filtered_items.append(item)
            except TypeError:
                continue
        return filtered_items
