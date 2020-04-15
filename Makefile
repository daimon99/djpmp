help:           ## Show this help.
	# @fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'
	@grep '^[a-zA-Z]' $(MAKEFILE_LIST) | sort | awk -F ':.*?## ' 'NF==2 {printf "\033[36m  %-25s\033[0m %s\n", $$1, $$2}'


init:  ## 初始化python环境，并加载测试数据
	python3 -m venv env
	env/bin/python -m pip install -r requirements.txt
	env/bin/python src/manage.py migrate
	env/bin/python src/manage.py loaddata --format yaml fixtures.yaml
	@echo "初始化完成。现在你可以运行：make run 启动后端应用了。"

init2: ## 简单建立 env/bin/python 来直接搭建环境
	mkdir -p env/bin
	ln -s `which python` env/bin/python
	ln -s `which python` env/bin/python3

stop: ## 停止 make prd/ make run 启动的服务
	-lsof -i:9091 | awk 'NR==2{print $$2}' | xargs kill

run: stop ## 运行后端服务(front)
	env/bin/python src/manage.py runserver 9091

prd: stop ## 生产环境运行(backend)
	nohup env/bin/python src/manage.py runserver 9091 2>&1 &

upgrade: ## 升级后端服务代码
	env/bin/python -m pip install -r requirements.txt
	env/bin/python src/manage.py migrate
	env/bin/python src/manage.py loaddata --format yaml fixtures.yaml
	env/bin/python src/manage.py collectstatic --noinput

dep: ## 部署服务到supervisor与nginx
	-sudo cp deploy/nginx/djpmp_prd.conf /etc/nginx/conf.d/
	-sudo cp deploy/supervisor/djpmp_prd.ini /etc/supervisord.d/

crontab: ## 安装 cron 定时任务
	cd src && ../env/bin/python manage.py installtasks

cloc: ## 代码量统计。请提前安装cloc(brew install cloc)
	cloc --exclude-dir="env,docs,logs,include,CMakeFiles,dist,static,theme,build,staticfiles" --exclude-ext="json,xml,yaml,yml,md" .

docker-build: ## docker build
	docker build -f docker/Dockerfile -t ccr.ccs.tencentyun.com/tjhb/djpmp:latest .

docker-run: ## docker run
	if [ -f .env ]; then docker run --env-file=.env --rm -it -p 9091:9091 ccr.ccs.tencentyun.com/tjhb/djpmp ${CMD} ; \
	else docker run --rm -it -p 9091:9091 ccr.ccs.tencentyun.com/tjhb/djpmp ${CMD} ; fi

docker-release: test docker-test ## merge master to docker
	bumpversion patch
# 	git checkout -B docker origin/docker
# 	git merge master
# 	git checkout master

release: docker-release # 发布到生产环境
	docker push ccr.ccs.tencentyun.com/tjhb/djpmp:latest
	git push --all

test: ## Smoke Test suit
	PYTHONPATH=./src pytest -m "smoke"

docker-test: ## test docker
	docker build -f ./docker/Dockerfile -t ccr.ccs.tencentyun.com/tjhb/djpmp:latest .

doc: ## 构建 doc 文档, 并查看
	cd docs && make open

epub: ## 构建 epub 模式文档
	cd docs && make epub && open -a finder _build/epub

pdf: ## 构建 pdf 文档
	cd docs && make pdf

doc-clean: ## 清理 doc 构建数据
	cd docs && make clean

%:  ## cli命令
	env/bin/python "cli.py" $(MAKECMDGOALS)
