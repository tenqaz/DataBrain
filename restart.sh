ps aux | grep /opt/DataBrain/DataBrain/app.py | awk {'print $2'} | xargs kill -9

poetry install

nohup poetry run python app.py > /dev/null &
