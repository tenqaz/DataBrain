### 简介
爬虫+可视化

数据源，通过爬虫获取数据
数据可视化

### 项目搭建
python3.8

1. 安装虚拟环境及所依赖的库
`pip install poetry`

`poetry install`   


2. 依赖于chrome
需要安装linux版chrome

将tools/chromedriver复制到/usr/bin中

3. 运行

运行爬虫程序，获取数据

`poetry run python spider.py`  

运行web可视化程序

`poetry run python app.py`

### 可视化web

#### url

* 拉勾网可视化数据

/DataBrain/web/index.html

### 规划
- 工作
    - 拉钩 (已做)
        - 每天的发布的岗位数量
        - 每天的岗位平均薪资
        - 不同语言的公司发布岗位的数量
    - boss
    - 51job
    
#### 项目待优化

- 环境变量
- uwsgi

