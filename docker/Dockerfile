FROM ccr.ccs.tencentyun.com/tjhb/docker-django2:latest

ARG PROJECT=djpmp

COPY ./requirements-docker.txt /data/prd/${PROJECT}/requirements-docker.txt
RUN pip install -r /data/prd/${PROJECT}/requirements-docker.txt

WORKDIR /data/prd/${PROJECT}

COPY . .
COPY ./src/config/config.example.py /data/prd/${PROJECT}/src/config/config.py

ENV TJHB_DEBUG="false" \
    SECRET="_uh0jj8&ge&xp_0^*n&ms_@)72pzlmx99-=4!7#esgdiq@%&#k" \
    DATABASE_URL="sqlite:///db.sqlite3" \
    CELERY_BROKER_URL="amqp://username:password@host:5672/xxx" \
    OPENAUTH_JWT_SECRET="" \
    QYWX_LOGIN_URL="https://open.taijihuabao.com/api/openauth/qywx?next="

ENTRYPOINT ["/data/prd/djpmp/docker-entrypoint.sh"]

#STOPSIGNAL SIGINT
EXPOSE 9091
VOLUME /data/prd/${PROJECT}/uploads /data/prd/${PROJECT}/staticfiles
