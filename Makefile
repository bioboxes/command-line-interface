path    := PATH=$(PWD)/.tox/py27-build/bin:$(shell echo "${PATH}")
version := $(shell $(path) python setup.py --version)
name    := $(shell $(path) python setup.py --name)
dist    := dist/$(name)-$(version).tar.gz

verifier-image := test-verify

NO_COLOR=\x1b[0m
OK_COLOR=\x1b[32;01m
ERROR_COLOR=\x1b[31;01m
WARN_COLOR=\x1b[33;01m

#################################################
#
# Publish the pip package
#
#################################################

publish: $(dist)
	@$(path) twine upload \
		--username ${PYPI_USERNAME} \
		--password ${PYPI_PASSWORD} \
		$^
	./plumbing/rebuild-site

clean:
	rm -rf dist *.egg-info

#################################################
#
# Run tests and features
#
#################################################

test      = tox -e py27-unit -e py3-unit -- $(ARGS)
autotest  = clear && $(test) -m \'not slow\'
wip       = clear && $(test) -m \'wip\'
ci        = clear && $(test) -m \'not noci\'
wip-found = $(shell find test -name '*.py' | xargs grep '@pytest.mark.wip')
feature   = tox -e py27-feature -e py3-feature -- $(ARGS)

command:
	@command -v realpath >/dev/null 2>&1 || { echo >&2 "Please install 'realpath' on your system"; exit 1; }

feature: tmp/tests command
	@$(feature)

ci_test:
	$(ci)

# "Work in Progress" unit tests
# Useful for testing only the code currently being developed
# Should not however be checked into version control
wip: tmp/tests command
	@$(wip)

test: tmp/tests command
	@if test -n "$(wip-found)"; then\
		echo "$(ERROR_COLOR)Work in progress tests found: '@pytest.mark.wip'. Please remove first.$(NO_COLOR)\n"; \
		exit 1; \
	fi
	@$(test)

autotest: tmp/tests
	@$(autotest) || true # Using true starts tests even on failure
	@fswatch \
		--exclude 'pyc' \
		--one-per-batch	./biobox_cli \
		--one-per-batch ./test \
		| xargs -n 1 -I {} bash -c "$(autotest)"

console:
	@$(path) python -i console.py

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


bootstrap: .images tmp/tests

.images: $(shell find images -name "*")
	docker pull bioboxes/crash-test-biobox@sha256:fdfdda8192dd919e6cac37366784ec8cfbf52c6fec53fe942a7f1940bd7642e8
	docker pull bioboxes/velvet
	docker pull bioboxes/quast
	docker build --tag $(verifier-image) images/$(verifier-image)
	touch $@

# Docker cannot access directories outside of the user home directory on OSX.
# This is because a virtual machine is used which has the user $HOME mounted
# into it
tmp/tests:
	mkdir -p $@

.PHONY: bootstrap build feature test-build publish test command
