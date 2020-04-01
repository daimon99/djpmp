贡献代码
=========

相关资源
--------

* 系统访问：
* 提需求：
* GIT库：
* 部署位置:
* 数据库：
* sentry:
* 沟通工具：

构建文档
---------

mac 下文档构建与浏览 ::

    cd docs
    make install-mac
    # 构建 html 文档
    make html
    # 构建 pdf
    # make pdf
    # 浏览文档
    make open

之后可以直接 `make open` 来构建并查看 `html` 格式文档

安装完构建文档的程序后，后面也可以直接在项目目录下运行 `make doc` 直接构建文档

如果要构建 `pdf` 文档，需要安装 macTex(文件大小：4G)，下载地址：

* 公网下载：http://file.taijihuabao.com/private/uploads/927a9bcd8864789c7f33dbd01f8eb8c9
* 内网下载：http://filei.taijihuabao.com/private/uploads/927a9bcd8864789c7f33dbd01f8eb8c9

构建文档时，如果你希望显示源码中包或模块级别的变量，注意注释方法 ::

    #: 注释前面加上 : 即可让该变量被 autodoc 模块识别
    demo_var = "这是一个测试"

具体可以参考：https://www.sphinx-doc.org/en/1.0/ext/autodoc.html#directive-autoattribute

关于 reStructure 文档的语法，可以参考：

* https://matplotlib.org/sampledoc/cheatsheet.html
* http://openalea.gforge.inria.fr/doc/openalea/doc/_build/html/source/sphinx/rest_syntax.html
* https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html#hyperlinks
* https://www.sphinx-doc.org/en/1.0/contents.html
* https://docutils.sourceforge.io/rst.html

关于 流程图 ``graphviz`` 的语法，参考：

* https://graphviz.gitlab.io/gallery/
* https://casatwy.com/shi-yong-dotyu-yan-he-graphvizhui-tu-fan-yi.html
* https://graphviz.readthedocs.io/en/stable/manual.html#jupyter-notebooks
* https://github.com/xflr6/graphviz/blob/master/examples/notebook.ipynb

如果要实时看效果，可以在 ``jupyter notebook`` 中看 ::

    from graphviz import Source
    doc = """
    digraph test1 {
        a -> b -> c;
    }
    Source(doc)
    """

注意修订文档后，请在 :ref:`VERSION` 章节中，注意补充修订信息。原则上每次对外发出的时候，必须升级一个版本号。如果自己改，没有对外发布，可不升级版本号。在原版本行上补充信息即可。

升级版本号时，需要做以下操作：

#. `VERSION` 文件中补充修订记录
#. `conf.py` 中的 `release` 字段修订

如果生成 `pdf` 文档，还要补充以下几步：

#. 把新生成的 `pdf` 文件 `copy` 到 `release` 文件夹中，归档。之后对外发布 `release` 文件夹中的文档

本机构建开发环境
----------------

配置文件
~~~~~~~~~

.. code-block::

    cp src/config/config.example.py src/config/config.py
    touch .env

之后请配置 `.env` 文件参数，决定连接哪个数据库 ::

    TJHB_DEBUG=True
    # 本地文件数据库
    DATABASE_URL=SQLITE:///db.sqlite3
    # 生产环境数据库
    # DATABASE_URL=psql://<username>:<password>@<db_ip>:<port>/<instance>

.. note::

    如果 数据库地址 无法连接，请联系 SRE工程师 ，提供 自己的公网IP，请其加入到 IP白名单中

安装与配置开发环境
~~~~~~~~~~~~~~~~~~~

完成全新的独立的构建一个 `python` 环境，不使用全局 `python` ::

    make init
    make upgrade
    make run

如果你的 `python` 默认是 `python3`，想用全局的 `python` 来构建，可以这样操作 ::

    make init2
    make upgrade
    make run


代码部署
--------

.. code-block:: bash

    make docker-release

`make docker-release` 背后的构建步骤是这样的：

.. graphviz::

    digraph build_flow {
        "打版本标签" -> "提交代码到docker分支" -> "触发腾讯云镜像库构建镜像"
        -> "触发腾讯云k8s群重新部署POD" -> "构建成功后发企业微信消息";
    }
