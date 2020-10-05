"""
@author: Jim
@project: DataBrain
@file: recorder.py
@time: 2020/10/4 11:24
@desc:  
    将爬取到的源数据记录到文件中
"""

from typing import List, Dict
import csv
from abc import ABCMeta, abstractmethod


class BaseRecorder:
    __metaclass__ = ABCMeta

    @abstractmethod
    def save(self, data):
        raise NotImplementedError


class FileRecorder(BaseRecorder):

    def __init__(self, file_name: str, field_list: List, sep: str = "\t"):
        self.__file_name = file_name

        self.__f = open(file_name, "a+", encoding="utf8")
        self.__csv_f = csv.DictWriter(self.__f, field_list, delimiter=sep)
        self.__csv_f.writeheader()

    def save(self, data: Dict):
        self.__csv_f.writerow(data)

    def __del__(self):
        self.__f.close()


class DataRecorder(BaseRecorder):

    def __init__(self):
        pass

    def save(self, data):
        pass
