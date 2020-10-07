"""
@author: Jim
@project: DataBrain
@file: base_crawler.py
@time: 2020/10/7 12:00
@desc:  
    
"""

from selenium import webdriver
import platform


class BaseCrawler:

    def __init__(self, query):
        self._query = query
        self._url = self.URL.format(self._query)

        self.__options = None
        self.__init_options()
        self._cur_page = 1

        self._driver = webdriver.Chrome(options=self.__options)

    def __init_options(self):
        """ 初始化chrome配置

        """
        if platform.system() == "Linux":
            self.__options = webdriver.ChromeOptions()
            self.__options.add_argument('headless')  # 浏览器不提供可视化页面
            self.__options.add_argument('no-sandbox')  # 解决DevToolsActivePort文件不存在的报错
            self.__options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
