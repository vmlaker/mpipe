.PHONY: venv

all: test

venv: requirements.txt
	virtualenv venv -p python3
	./venv/bin/pip install -r requirements.txt

test: venv
	./venv/bin/python setup.py build
	./venv/bin/python setup.py install
	./venv/bin/python setup.py test

docs: test
	cd doc && mkdir -p build/html
	cd doc && ../venv/bin/python create.py build

clean:
	rm -rf build dist venv
	rm -rf doc/build
	rm -rf doc/venv
	rm -rf src/*.pyc
	rm -rf src/__pycache__
	rm -rf test/*.out
