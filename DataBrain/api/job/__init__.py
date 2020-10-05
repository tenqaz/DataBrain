"""
@author: Jim
@project: DataBrain
@file: __init__.py.py
@time: 2020/10/5 11:52
@desc:  
    
"""

from flask import Flask
from flask.blueprints import Blueprint

from . import lagou


def init_blueprint_job(app: Flask):
    job_blu = Blueprint("job", __name__)
    lagou.api.register(job_blu)
    app.register_blueprint(job_blu, url_prefix="/job")
