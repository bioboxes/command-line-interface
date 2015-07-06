bootstrap: vendor/python

vendor/python: requirements.txt
	mkdir -p log
	virtualenv $@ 2>&1 > log/virtualenv.txt
	$@/bin/pip install -r $< 2>&1 > log/pip.txt
	touch $@
