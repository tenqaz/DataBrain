ps aux | grep /opt/DataBrain/DataBrain/app.py | awk {'print $2'} | xargs kill -9

git pull

nohup poetry run python app.py > /dev/null &