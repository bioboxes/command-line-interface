path    := PATH=./vendor/python/bin:$(shell echo "${PATH}")
version := $(shell $(path) python setup.py --version)
name    := $(shell $(path) python setup.py --name)
dist    := dist/$(name)-$(version).tar.gz

installer-image := test-install
verifier-image  := test-verify

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


test    = $(path) nosetests --rednose

command:
	@command -v realpath >/dev/null 2>&1 || { echo >&2 "Please install 'realpath' on your system"; exit 1; }

feature: command
	@$(path) behave --stop $(ARGS)

test: command
	@$(test)

autotest:
	@clear && $(test) || true # Using true starts tests even on failure
	@fswatch -o ./biobox_cli -o ./test | xargs -n 1 -I {} bash -c "clear && $(test)"


#################################################
#
# Build and test the pip package
#
#################################################


build: $(dist) test-build

test-build: $(dist)
	docker run \
		--tty \
		--volume=$(abspath $(dir $^)):/dist:ro \
		$(installer-image) \
		/bin/bash -c "pip install --user /$^ && clear && /root/.local/bin/biobox -h"

ssh: $(dist)
	docker run \
		--interactive \
		--tty \
		--volume=$(abspath $(dir $^)):/dist:ro \
		$(installer-image) \
		/bin/bash -c "pip install --user /$^ && clear && bash"

$(dist): $(shell find biobox_cli) requirements.txt setup.py MANIFEST.in
	$(path) python setup.py sdist
	touch $@


#################################################
#
# Bootstrap project requirements for development
#
#################################################


bootstrap: vendor/python .images

vendor/python: requirements.txt
	mkdir -p log
	virtualenv $@ 2>&1 > log/virtualenv.txt
	$(path) pip install -r $< 2>&1 > log/pip.txt
	touch $@

.images: requirements.txt $(shell find images -name "*")
	docker pull bioboxes/velvet
	docker pull bioboxes/megahit
	cp $< images/test-install
	docker build --tag $(installer-image) images/$(installer-image)
	docker build --tag $(verifier-image)  images/$(verifier-image)
	touch $@

.PHONY: bootstrap build feature test-build publish test command
