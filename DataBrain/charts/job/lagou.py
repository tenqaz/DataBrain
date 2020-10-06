"""
@author: Jim
@project: DataBrain
@file: job.py
@time: 2020/10/5 14:12
@desc:  
    
"""

import datetime

from pyecharts import options as opts
from pyecharts.charts import Pie, Bar

from models.job import BaseJobModel


def create_publish_num_pie(publish_num):
    """ 创建昨日发布数量

    """

    pie_data = BaseJobModel.publish_num(publish_num)

    c = Pie(init_opts=opts.InitOpts(width="1600px", height="800px", bg_color="#2c343c")).add(
        series_name="{}编程语言发布数量".format(publish_num),
        data_pair=pie_data,
        rosetype="radius",
        radius="55%",
        center=["50%", "50%"],
        label_opts=opts.LabelOpts(is_show=False, position="center"),
    ).set_global_opts(
        title_opts=opts.TitleOpts(
            title="{}编程语言发布数量".format(publish_num),
            pos_left="center",
            pos_top="20",
            title_textstyle_opts=opts.TextStyleOpts(color="#fff"),
        ),
        legend_opts=opts.LegendOpts(is_show=False),
    ).set_series_opts(
        tooltip_opts=opts.TooltipOpts(
            trigger="item", formatter="{a} <br/>{b}: {c} ({d}%)"
        ),
        label_opts=opts.LabelOpts(color="rgba(255, 255, 255, 0.3)", formatter="{b}: {c}"),
    )

    return c


def create_avg_salary(publish_time):

    results = BaseJobModel.avg_salary(publish_time)

    keywords = []
    low_salarys = []
    high_salarys = []
    avg_salary = []
    for record in results:
        keywords.append(record['_id'])
        low_salarys.append(record["low_salary"])
        high_salarys.append(record['high_salary'])
        avg_salary.append((record["low_salary"] + record['high_salary']) / 2)

    c = (
        Bar().add_xaxis(
            keywords
        ).add_yaxis(
            "最低平均工资", low_salarys
        ).add_yaxis(
            "最高平均工资", high_salarys
        ).add_yaxis(
            "平均工资", avg_salary
        ).set_global_opts(
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-15)),
            title_opts=opts.TitleOpts(title="{} 各个编程语言的平均工资".format(publish_time), subtitle=""),
        )
    )
    return c
