"""
@author: Jim
@project: DataBrain
@file: job.py
@time: 2020/10/3 11:33
@desc:  拉钩直聘爬虫
    
"""

import datetime

from loguru import logger
from parse import search
from pyquery import PyQuery as pq
from selenium.common import exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from core.exceptions import StopException
from crawler.base_crawler import BaseCrawler
from models.job import BaseJob, JobSourceEnum, BaseJobModel


class LagouCrawler(BaseCrawler):
    URL = "https://www.lagou.com/jobs/list_{}/p-city_215?px=new"
    TODAY = True  # 仅爬取当天发布的
    TIMEOUT = 5

    def __init__(self, query):
        super().__init__(query)

        today = datetime.date.today()
        self.__exist_page_ids = BaseJobModel.get_page_ids_by_publish_time(today)

    def __parse_list(self):
        """ 解析列表

        """

        # 可能有弹窗，关闭
        try:
            WebDriverWait(self._driver, self.TIMEOUT).until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "body > div.body-container.showData > div > div.body-btn")))
            self._driver.find_element_by_css_selector(
                "body > div.body-container.showData > div > div.body-btn").click()
        except exceptions.TimeoutException:
            pass

        # 进入详细页
        for record in self._driver.find_elements_by_css_selector(".item_con_list .position_link"):
            record.send_keys(Keys.ENTER)

            self._driver.switch_to.window(self._driver.window_handles[-1])
            self.__detail_page()
            self._driver.close()
            self._driver.switch_to.window(self._driver.window_handles[0])

    def __next_page(self):
        """ 下一页

        """
        try:
            WebDriverWait(self._driver, self.TIMEOUT).until(
                EC.presence_of_element_located((By.CLASS_NAME, "pager_next")))
        except exceptions.TimeoutException:
            logger.debug("没有找到下一页")
            raise StopException()

        try:
            self._driver.find_element_by_class_name("pager_next_disabled")
        except exceptions.NoSuchElementException:
            pass
        else:
            raise StopException()

        self._driver.find_element_by_css_selector(".pager_next").click()
        self._cur_page += 1

    def __detail_page(self):
        """ 跳转到细节页

        """
        page_id = search("/jobs/{page_id}.html", self._driver.current_url)['page_id']

        try:
            WebDriverWait(self._driver, self.TIMEOUT).until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "body > div.position-head > div > div.position-content-l > div > h1 > span > span")))
        except exceptions.TimeoutException:
            logger.debug("page_id = {} 没有加载".format(page_id))
            return

        logger.debug("正在爬取page_id = {}".format(page_id))
        if page_id in self.__exist_page_ids:
            logger.debug("page_id = {} 已爬取过，停止该keyword爬取".format(page_id))
            raise StopException()

        page_html = self._driver.page_source
        doc = pq(page_html)

        publish_time = doc("body > div.position-head > div > div.position-content-l > dd > p").text()  # 发布时间
        publish_time = search("{:^}发布于", publish_time)[0]
        if ":" in publish_time:
            publish_time = str(datetime.date.today())
        elif self._driver.find_elements_by_class_name("wise-icon"):  # 如果是急招，则跳过本条
            return
        elif self.TODAY:
            logger.debug("不是该天的数据，停止")
            raise StopException()

        # 职位名称
        name = doc("body > div.position-head > div > div.position-content-l > div > h1 > span > span").text()

        # 薪水
        salary = doc("body > div.position-head > div > div.position-content-l > dd > h3 > span.salary").text().replace(
            "k", "")
        salary_split = salary.split("·")
        low_salary, high_salary = salary_split[0].split("-")
        try:
            salary_num = salary_split[1]
            salary_num = salary_num.replace("薪", "")
        except IndexError:
            salary_num = 12

        city = doc("body > div.position-head > div > div.position-content-l > dd > h3 > span:nth-child(2)").text()
        work_experience = doc(
            "body > div.position-head > div > div.position-content-l > dd > h3 > span:nth-child(3)").text()
        education = doc("body > div.position-head > div > div.position-content-l > dd > h3 > span:nth-child(4)").text()
        job_detail = doc("#job_detail > dd.job_bt > div").text()

        # 全职/兼职
        work_type = doc("body > div.position-head > div > div.position-content-l > dd > h3 > span:nth-child(5)").text()

        # 职业标签
        tag_doc = doc("body > div.position-head > div > div.position-content-l > dd > ul > li")
        tags = []
        for tag in tag_doc.items():
            tags.append(tag.text())

        # 工作城市
        work_city = doc("#job_detail > dd.job-address.clearfix > div.work_addr > a:nth-child(1)").text()
        # 工作地区
        work_district = doc("#job_detail > dd.job-address.clearfix > div.work_addr > a:nth-child(2)").text()
        # 工作区域
        work_area = doc("#job_detail > dd.job-address.clearfix > div.work_addr > a:nth-child(3)").text()

        company_name = doc("#job_company > dt > a > div > h3 > em").text()
        company_domain = doc("#job_company > dd > ul > li:nth-child(1) > h4").text()
        company_develop_level = doc("#job_company > dd > ul > li:nth-child(2) > h4").text()
        company_size = doc("#job_company > dd > ul > li:nth-child(3) > h4").text()  # 规模
        company_index = doc("#job_company > dd > ul > li:nth-child(4) > a").text()  # 网址

        BaseJob(name=name, low_salary=low_salary, high_salary=high_salary, salary_num=salary_num, city=city,
                work_experience=work_experience, education=education, job_detail=job_detail,
                publish_time=publish_time, work_type=work_type, tags=tags, work_city=work_city,
                work_district=work_district, work_area=work_area, company_name=company_name,
                company_domain=company_domain, company_develop_level=company_develop_level, company_size=company_size,
                company_index=company_index, keyword=self._query, origin=JobSourceEnum.LAGOU.value,
                page_id=page_id).save()

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
