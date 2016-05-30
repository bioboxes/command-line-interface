path    := PATH=$(PWD)/vendor/$(PYTHON_VERSION)/bin:$(shell echo "${PATH}")
version := $(shell $(path) python setup.py --version)
name    := $(shell $(path) python setup.py --name)
dist    := dist/$(name)-$(version).tar.gz

python-3-image := py3
python-2-image := py2
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
feature  = tox -e py27-feature -e py3-feature

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


build: $(dist) .test-build-py2 .test-build-py3

.test-build-py3: ./plumbing/test-pip-install $(dist)
	@$^ $(python-2-image)
	@touch $@

.test-build-py2: ./plumbing/test-pip-install $(dist)
	@$^ $(python-3-image)
	@touch $@

ssh: $(dist)
	docker run \
		--interactive \
		--tty \
		--volume=$(abspath $(dir $^)):/dist:ro \
		$(python-2-image) \
		/bin/bash -c "pip install --user /$^ && clear && bash"

$(dist): $(shell find biobox_cli) requirements.txt setup.py MANIFEST.in
	$(path) python setup.py sdist
	touch $(dir $@)

#################################################
#
# Bootstrap project requirements for development
#
#################################################


bootstrap: .tox .images

.tox: requirements.txt
	tox --notest
	@touch $@

.images: requirements.txt $(shell find images -name "*")
	docker pull bioboxes/velvet
	cp $< images/$(python-2-image)
	docker build --tag $(python-2-image) images/$(python-2-image)
	docker build --tag $(python-3-image) images/$(python-3-image)
	docker build --tag $(verifier-image) images/$(verifier-image)
	touch $@

.PHONY: bootstrap build feature test-build publish test command
