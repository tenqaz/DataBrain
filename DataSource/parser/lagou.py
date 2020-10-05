"""
@author: Jim
@project: DataBrain
@file: job.py
@time: 2020/10/4 18:21
@desc:
    拉勾网数据统计结果入库
    
"""

import pandas as pd


class LagouParser:

    def __init__(self, storage_path):
        self.__storage_path = storage_path

    def publish_today(self):
        """ 每个语言发布岗位的数量

        """
        df = pd.read_csv(self.__storage_path, sep="\t")
        df['keyword'].value_counts()


    def run(self):
        self.publish_today()
