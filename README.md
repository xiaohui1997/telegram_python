# telegram_python
python-telegram-bot.org 13.1

#### 基础环境
```bash
yum install python3-devel
pip3 install -r requirements.txt -i https://mirrors.163.com/pypi/simple/
mkdir /var/log/uwsgi
uwsgi uwsgi.ini
#### 停止项目
uwsgi --stop /var/log/uwsgi/uwsgi.pid
```