python_version := 3.5

virtual:
	pyvenv-$(python_version) virtual
	# https://github.com/klen/python-mode/issues/406
	mkdir -p virtual/Scripts
	touch virtual/Scripts/activate_this.py

test:
	py.test --cov not_the_sparrow check
