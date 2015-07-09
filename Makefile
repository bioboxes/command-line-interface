path    := PATH=./vendor/python/bin:$(shell echo "${PATH}")
version := $(shell $(path) python setup.py --version)

publish: $(build)
	@$(path) twine upload \
		--username ${PYPI_USERNAME} \
		--password ${PYPI_PASSWORD} \
		$^

console:
	@$(path) python -i console.py

#################################################
#
# Run tests and features
#
#################################################


test    = $(path) nosetests --rednose

feature:
	@$(path) behave features

test:
	@$(test)

autotest:
	@clear && $(test) || true # Using true starts tests even on failure
	@fswatch -o ./biobox_cli -o ./test | xargs -n 1 -I {} bash -c "clear && $(test)"


#################################################
#
# Build and test the pip package
#
#################################################


build   := dist/biobox_cli-$(version).tar.gz

build: $(build) test-build

test-build: $(build)
	docker run \
		--volume=$(abspath $(dir $^)):/dist:ro \
		python:2.7 \
		/bin/bash -c "pip install --user /$^ && /root/.local/bin/biobox -h"

$(build): $(shell find biobox_cli) requirements.txt setup.py MANIFEST.in
	$(path) python setup.py sdist
	touch $@


#################################################
#
# Bootstrap project requirements for development
#
#################################################


bootstrap: vendor/python .image

vendor/python: requirements.txt
	mkdir -p log
	virtualenv $@ 2>&1 > log/virtualenv.txt
	$(path) pip install -r $< 2>&1 > log/pip.txt
	touch $@

.image:
	docker pull python:2.7
	docker pull bioboxes/velvet
	touch $@

.PHONY: bootstrap build feature test-build publish test
