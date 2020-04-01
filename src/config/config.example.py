# coding: utf-8
# 经常调整的配置文件参数

import environ
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

env = environ.Env()
env.read_env(os.path.join(BASE_DIR, '.env'))

TJHB_DEBUG = env.bool('TJHB_DEBUG', default=False)
SECRET_KEY = env.bool('SECRET_KEY', default='_uh0jj8&ge&xp_0^*n&ms_@)72pzlmx99-=4!7#esgdiq@%&#k')
DATABASE_URL = env.db_url('DATABASE_URL', default='sqlite:///db.sqlite3')
CELERY_BROKER_URL = env('CELERY_BROKER_URL', default='amqp://username:password@host:5672/xxx')
OPENAUTH_JWT_SECRET = env('OPENAUTH_JWT_SECRET', default='')
QYWX_LOGIN_URL = env("QYWX_LOGIN_URL", default="https://open.taijihuabao.com/api/openauth/qywx?next=")
