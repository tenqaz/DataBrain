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


class BaseLagouModel:

    @staticmethod
    def publish_num(publish_time):
        """ 查询，根据keyword分组，发布的数量

        Args:
            publish_time:

        Returns:

        """
        pipline = [
            {
                "$group": {
                    "_id": "$keyword",
                    "num": {"$sum": 1}
                }
            }
        ]

        results = BaseLagou.objects(publish_time=publish_time).aggregate(pipline)

        data = [(record['_id'], record['num']) for record in results]
        return data

    @staticmethod
    def avg_salary(publish_time):
        """ 查询，根据keyword分组, 平均工资

        Args:
            publish_time: 发布时间

        Returns:

        """
        pipline = [
            {
                "$group": {
                    "_id": "$keyword",
                    "low_salary": {"$avg": "$low_salary"},
                    "high_salary": {"$avg": "$high_salary"}
                }
            }
        ]

        results = BaseLagou.objects(publish_time=publish_time).aggregate(pipline)

        return results


if __name__ == '__main__':
    from mongoengine import connect

    connect("DataBrain")
    now_day = str(datetime.date.today())

    print(list(BaseLagouModel.avg_salary(now_day)))
    print(list(BaseLagouModel.publish_num(now_day)))