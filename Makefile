python_version := 3.5

default: test

virtual:
	pyvenv-$(python_version) virtual
	# https://github.com/klen/python-mode/issues/406
	mkdir -p virtual/Scripts
	touch virtual/Scripts/activate_this.py

test:
	flake8 not_the_sparrow test
	py.test --verbose --cov not_the_sparrow

lint:
	pylint not_the_sparrow test/*.py

.PHONY: default test lint
