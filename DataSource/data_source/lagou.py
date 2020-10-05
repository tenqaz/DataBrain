"""
@author: Jim
@project: DataBrain
@file: job.py
@time: 2020/10/4 19:21
@desc:  
    
"""

from crawler.lagou import LagouCrawler
import datetime
import os
import platform

class BossDataSource:

    DATA_LINUX_PATH = "/data/databrain/job"
    DATA_WINDOWS_PATH = ".."

    def __init__(self):
        self.__keywords = ["python", "java", "c", "c++", "php", "go"]


        file_name = "lagou_{}.csv".format(datetime.date.today())
        path = self.DATA_LINUX_PATH if platform.system() == "Linux" else self.DATA_WINDOWS_PATH
        self.__storage_path = os.path.join(path, file_name)

    def run(self):
        pass

        # 爬
        # for keyword in self.__keywords:
        #     lagou_crawler = LagouCrawler(keyword, self.__storage_path)
        #     lagou_crawler.crawler()

        # 统计结果


if __name__ == '__main__':
    BossDataSource.run()