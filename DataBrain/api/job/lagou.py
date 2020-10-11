"""
@author: Jim
@project: DataBrain
@file: job.py
@time: 2020/10/5 11:52
@desc:  
    
"""

from charts.job.lagou import create_publish_num_pie, create_avg_salary, company_publish_count_by_language
from libs.redprint import Redprint
from flask import request
import datetime

api = Redprint("lagou")


@api.route("/publish_num_pie")
def publish_num_pie():
    last_day = str(datetime.datetime.today() - datetime.timedelta(days=1))
    publish_time = request.args.get("publish_time", last_day)

    c = create_publish_num_pie(publish_time)
    return c.dump_options_with_quotes()


@api.route("/avg_salary_bar")
def avg_salary_bar():
    last_day = str(datetime.datetime.today() - datetime.timedelta(days=1))
    publish_time = request.args.get("publish_time", last_day)

    c = create_avg_salary(publish_time)
    return c.dump_options_with_quotes()


@api.route("/publush_num_company")
def publush_num_company():
    last_day = str(datetime.datetime.today() - datetime.timedelta(days=1))
    publish_time = request.args.get("publish_time", last_day)
    language = request.args.get("language", "python")

    c = company_publish_count_by_language(publish_time, language)
    return c.dump_options_with_quotes()
