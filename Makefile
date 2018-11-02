venv:
	virtualenv venv
	./venv/bin/python setup.py build
	./venv/bin/python setup.py install

test: venv
	./venv/bin/python setup.py test

clean:
	rm -rf build dist venv
	rm -rf doc/build
	rm -rf doc/venv
	rm -rf src/*.pyc
	rm -rf test/*.out
