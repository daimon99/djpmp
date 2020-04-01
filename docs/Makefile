# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
.PHONY: help Makefile

SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)


view: patch1
	open _build/latex/太*.pdf

patch1:
	# cd _build/latex;sed -ig 's/date{.*}/date{2019 年 9 月 5 日}/' *.tex;make
	-cd _build/latex;make > /dev/null 2>&1
	# 由于graphviz.pdf的存在，导致.ind文件不能正确生成（猜测），因此这里手工生成这个文件，以正确生成 pdf 因此这里手工生成这个文件
	cd _build/latex;ls 太* | awk "NR==1{print $1}" | sed 's/.aux/.ind/' | xargs touch
	cd _build/latex;make

clean:
	-rm -rf _build

pdf: clean latex view
	# 构建完成

open: html
	open _build/html/index.html

install-mac:
	pip install -r requirements.txt
	brew install graphviz

png: ## generate model png
	cd ..;python src/manage.py graph_models djpmp -E -o docs/img/model-djpmp.png -X Department,TimeStampedModel -n

html: 
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
