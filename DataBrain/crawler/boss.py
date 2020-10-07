"""
@author: Jim
@project: DataBrain
@file: boss.py
@time: 2020/10/7 11:59
@desc:  boss直聘
    
"""

import datetime
import re

from loguru import logger
from pyquery import PyQuery as pq
from selenium.common import exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from core.exceptions import StopException
from crawler.base_crawler import BaseCrawler
from models.job import BaseJob, JobSourceEnum, BaseJobModel


class BossCrawler(BaseCrawler):
    URL = "https://www.zhipin.com/c101280600/?query={}&page=1&ka=page-1"

    def __init__(self, query):
        pass
        # super().__init__(query)

    def _detail_page(self):

        # try:
        #     WebDriverWait(self._driver, self.TIMEOUT).until(EC.presence_of_element_located(
        #         (By.CSS_SELECTOR, "#main > div.job-banner > div > div > div.info-primary > div.name > h1")))
        # except exceptions.TimeoutException:
        #     logger.debug("page_id = {} 没有加载")
        #     return
        #
        # page_id = re.search("/job_detail/(.*?)~.html", self._driver.current_url).group(1)
        # logger.debug("正在爬取page_id = {}".format(page_id))
        #
        # page_html = self._driver.page_source
        with open("test.html", "r", encoding="utf8") as f:
            page_html = f.read()

        doc = pq(page_html)

        # 最后更新时间
        last_update_time = doc("#main > div.job-box > div > div.job-sider > div.sider-company > p.gray").text()
        last_update_time = re.search("更新于：(.*?)", last_update_time).group(1)

        # 职位名称
        name = doc("#main > div.job-banner > div > div > div.info-primary > div.name > h1").text()

        # 薪水
        salary = doc("#main > div.job-banner > div > div > div.info-primary > div.name > span").text().replace(
            "k", "")
        salary_split = salary.split("·")
        low_salary, high_salary = salary_split[0].split("-")
        try:
            salary_num = salary_split[1]
            salary_num = salary_num.replace("薪", "")
        except IndexError:
            salary_num = 12

        city = doc("#main > div.job-banner > div > div > div.info-primary > p > a").text()
        work_experience = doc("#main > div.job-banner > div > div > div.info-primary > p > em:nth-child(2)")
        work_experience = re.search("/>(.*)", str(work_experience)).group(1)

        education = doc("#main > div.job-banner > div > div > div.info-primary > p > em:nth-child(3)")
        education = re.search("/>(.*)", str(education)).group(1)

        job_detail = doc("#main > div.job-box > div > div.job-detail > div.detail-content > div:nth-child(1) > div").text()

        # 全职/兼职
        work_type = "全职"  # 默认

        # 职业标签
        tag_doc = doc("#main > div.job-banner > div > div > div.info-primary > div.tag-container > div.job-tags > span")
        tags = []
        for tag in tag_doc.items():
            tags.append(tag.text())

        # 工作城市
        work_city = doc("#job_detail > dd.job-address.clearfix > div.work_addr > a:nth-child(1)").text()

        # 工作地区
        # work_district = doc("#job_detail > dd.job-address.clearfix > div.work_addr > a:nth-child(2)").text()
        # # 工作区域
        # work_area = doc("#job_detail > dd.job-address.clearfix > div.work_addr > a:nth-child(3)").text()
        #
        # company_name = doc("#job_company > dt > a > div > h3 > em").text()
        # company_domain = doc("#job_company > dd > ul > li:nth-child(1) > h4").text()
        # company_develop_level = doc("#job_company > dd > ul > li:nth-child(2) > h4").text()
        # company_size = doc("#job_company > dd > ul > li:nth-child(3) > h4").text()  # 规模
        # company_index = doc("#job_company > dd > ul > li:nth-child(4) > a").text()  # 网址
        #
        # BaseJob(name=name, low_salary=low_salary, high_salary=high_salary, salary_num=salary_num, city=city,
        #         work_experience=work_experience, education=education, job_detail=job_detail,
        #         publish_time=publish_time, work_type=work_type, tags=tags, work_city=work_city,
        #         work_district=work_district, work_area=work_area, company_name=company_name,
        #         company_domain=company_domain, company_develop_level=company_develop_level, company_size=company_size,
        #         company_index=company_index, keyword=self._query, origin=JobSourceEnum.LAGOU.value,
        #         page_id=page_id).save()

    def __parse_list(self):

        # 进入详细页
        for record in self._driver.find_elements_by_css_selector(".job-list .job-name a"):
            record.send_keys(Keys.ENTER)

            self._driver.switch_to.window(self._driver.window_handles[-1])
            self.__detail_page()
            self._driver.close()
            self._driver.switch_to.window(self._driver.window_handles[0])

    def crawler(self):
        logger.debug("crawler {}".format(self._query))
        # 首页
        self._driver.get(self._url)

        while True:
            logger.debug("cur_page = {}".format(self._cur_page))

            try:
                self.__parse_list()
                self.__next_page()
            except StopException:
                break

        self._driver.quit()

if __name__ == '__main__':
    p = BossCrawler("python")
    p._detail_page()
    # print(p.crawler())