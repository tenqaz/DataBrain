"""
@author: Jim
@project: DataBrain
@file: main.py
@time: 2020/10/4 18:51
@desc:  
    
"""

from crawler.lagou import LagouCrawler

keywords = ["python",  "php", "go", "c", "c++"]
for keyword in keywords:
    lagou = LagouCrawler(keyword)
    lagou.crawler()
