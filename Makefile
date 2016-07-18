path    := PATH=$(PWD)/.tox/py27-build/bin:$(shell echo "${PATH}")
version := $(shell $(path) python setup.py --version)
name    := $(shell $(path) python setup.py --name)
dist    := dist/$(name)-$(version).tar.gz

verifier-image := test-verify

publish: $(dist)
	@$(path) twine upload \
		--username ${PYPI_USERNAME} \
		--password ${PYPI_PASSWORD} \
		$^
	./plumbing/rebuild-site

console:
	@$(path) python -i console.py

clean:
	rm -rf dist *.egg-info

#################################################
#
# Run tests and features
#
#################################################

test     = tox -e py27-unit -e py3-unit
autotest = clear && $(test)
feature  = tox -e py27-feature -e py3-feature $(ARGS)

command:
	@command -v realpath >/dev/null 2>&1 || { echo >&2 "Please install 'realpath' on your system"; exit 1; }

feature: command
	@$(feature)

test: command
	@$(test)

autotest:
	@$(autotest) || true # Using true starts tests even on failure
	@fswatch \
		--exclude 'pyc' \
		--one-per-batch	./biobox_cli \
		--one-per-batch ./test \
		| xargs -n 1 -I {} bash -c "$(autotest)"

#################################################
#
# Build and test the pip package
#
#################################################

build: $(dist) test-build

test-build:
	tox -e py27-build,py3-build

$(dist): $(shell find biobox_cli) requirements/default.txt setup.py MANIFEST.in
	@$(path) python setup.py sdist --formats=gztar
	touch $@

#################################################
#
# Bootstrap project requirements for development
#
#################################################


bootstrap: .tox .images

.tox: requirements/default.txt requirements/development.txt
	@tox --notest
	@touch $@

.images: $(shell find images -name "*")
	docker pull bioboxes/velvet
	docker build --tag $(verifier-image) images/$(verifier-image)
	touch $@

.PHONY: bootstrap build feature test-build publish test command
