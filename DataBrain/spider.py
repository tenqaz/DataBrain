"""
@author: Jim
@project: DataBrain
@file: spider.py
@time: 2020/10/4 18:51
@desc:  
    
"""

from mongoengine import connect
from loguru import logger
import platform
from core.setting import Config
from crawler.lagou import LagouCrawler

if platform.system == "Linux":
    logger.add("/var/log/DataBrain.log")

connect(Config.MONGODB_DB)

keywords = ["python", "php", "go", "c", "c++", "java"]
for keyword in keywords:
    lagou = LagouCrawler(keyword)
    lagou.crawler()
