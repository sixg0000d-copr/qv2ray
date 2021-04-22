MAKEFILE_DIR := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
PROJECT_ROOT := $(abspath $(MAKEFILE_DIR)/..)

spec ?= $(PROJECT_ROOT)/qv2ray.spec
outdir ?= $(PROJECT_ROOT)/outdir
source0 = $(shell spectool -s 0 $(spec) | awk '/Source0:/ { print $$2 }')
name-version = $(shell basename -s .tar.gz $(source0))
tag = $(shell awk '/%global tag/ { print $$3 }' $(spec))
branch = $(shell awk '/%global branch/ { print $$3 }' $(spec))
commit = $(shell awk '/%global commit/ { print $$3 }' $(spec))
committish = $(or $(or $(tag), $(branch)), $(commit))


all: srpm

$(outdir):
	[ -d "$(outdir)" ] || mkdir -p $(outdir)

ifeq ($(shell id -u),0)
init:
	dnf -y install git rpmdevtools
else
init:
	sudo dnf -y install git rpmdevtools
endif

.ONESHELL:
$(outdir)/$(source0): init $(outdir)
	cd $(outdir)
	git clone https://github.com/Qv2ray/Qv2ray $(name-version)
	cd $(name-version)
	git checkout $(committish)
	git submodule update --init --recursive
	cd ..
	tar czf $(source0) --exclude .git $(name-version)
	rm -rf $(name-version)

srpm: init $(outdir)/$(source0)
	rpmbuild \
	--define "_sourcedir $(outdir)" \
	--define "_srcrpmdir $(outdir)" \
	-bs $(spec)

clean:
	rm -rf $(outdir)

.PHONY: all init srpm clean
