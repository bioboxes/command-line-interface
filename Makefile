python  := ./vendor/python/bin/python
version := $(shell $(python) setup.py --version)
build   := dist/biobox_cli-$(version).tar.gz

build: $(build)

$(build): $(shell find biobox_cli) requirements.txt setup.py
	$(python) setup.py sdist
	touch $@

bootstrap: vendor/python

vendor/python: requirements.txt
	mkdir -p log
	virtualenv $@ 2>&1 > log/virtualenv.txt
	$@/bin/pip install -r $< 2>&1 > log/pip.txt
	touch $@
