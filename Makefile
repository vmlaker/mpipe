venv:
	virtualenv venv
	./venv/bin/python setup.py build
	./venv/bin/python setup.py install

test: venv
	./venv/bin/python setup.py test
