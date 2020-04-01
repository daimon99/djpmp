#!/usr/bin/env python
# coding: utf-8

import logging
import os
import socket
import subprocess
import sys

import click
import django
import requests
from django.conf import settings
from django.utils.timezone import now

QYWX_NOTIFY_URL = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=<请自己申请 key>'

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
django.setup()

log = logging.getLogger(__name__)


@click.group()
def main():
    pass


@main.command()
def mm():
    """make migration and migrate it."""
    click.secho('make migrations...', fg='yellow')
    subprocess.call('python src/manage.py makemigrations', shell=True)
    click.secho('migrate...', fg='yellow')
    subprocess.call('python src/manage.py migrate', shell=True)


@main.command()
def ok():
    """通知服务ok"""
    # 发送启动通知
    qywx_notice_key = "<robot key>"
    if qywx_notice_key != "<robot key>":
        requests.post(
            QYWX_NOTIFY_URL,
            json={
                "msgtype": "text",
                "text": {
                    "content": f"djpmp [{settings.VERSION}] 服务重启完成: {socket.gethostname()}, {now().astimezone()}"
                }})
    else:
        print("If you want to get a notice after deploy, please provide a key in the above.")


@main.command()
def fail():
    """发送失败通知"""
    # 发送启动通知
    requests.post(
        QYWX_NOTIFY_URL,
        json={
            "msgtype": "text",
            "text": {
                "content": f"djpmp [{settings.VERSION}]  代码更新失败，请检查服务！ {socket.gethostname()}, {now().astimezone().strftime('%Y/%m/%d %H:%M:%S')}"
            }})


@main.command()
def backup():
    """基础数据备份"""
    import subprocess
    subprocess.getoutput(
        "python src/manage.py dumpdata --format yaml auth openauth djpmp > fixtures-backup.yaml ")


if __name__ == '__main__':
    main()
