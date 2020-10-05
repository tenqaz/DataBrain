"""
@author: Jim
@project: DataBrain
@file: app.py
@time: 2020/10/4 18:27
@desc:  
    
"""

from flask import Flask
from flask_cors import CORS
from mongoengine import connect

from api.job import init_blueprint_job
from core.setting import Config


def create_app():
    app = Flask(__name__, static_folder="templates")
    app.config.from_object(Config)

    init_blueprint_job(app)

    connect(app.config.get("MONGODB_DB"))

    CORS(app)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
