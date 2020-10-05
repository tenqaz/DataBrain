"""
@author: Jim
@project: DataBrain
@file: job.py
@time: 2020/10/4 23:13
@desc:  
    
"""

import datetime

from mongoengine import Document, StringField, IntField, ListField, DateTimeField, DateField


class BaseLagou(Document):
    name = StringField()
    low_salary = IntField()
    high_salary = IntField()
    salary_num = IntField()
    city = StringField()
    work_experience = StringField()
    education = StringField()
    job_detail = StringField()
    publish_time = DateField()
    work_type = StringField()
    tags = ListField()
    work_city = StringField()
    work_district = StringField()
    work_area = StringField()
    company_name = StringField()
    company_domain = StringField()
    company_develop_level = StringField()
    company_size = StringField()
    company_index = StringField()
    keyword = StringField()
    create_time = DateTimeField(default=datetime.datetime.utcnow)

