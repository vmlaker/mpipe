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

dist: clean venv
	./venv/bin/python setup.py sdist

testpypi: dist
	./venv/bin/twine upload --repository testpypi dist/*

pypi: dist
	./venv/bin/twine upload dist/*

MASTER_VERSION = $(shell git log master -1 | head -1)

gh-pages: docs
	rm -rf html
	#git clone https://github.com/vmlaker/mpipe.git html
	git clone git@github.com:vmlaker/mpipe.git html
	cd html && git checkout gh-pages
	rm -rf html/*
	cp -r doc/build/html/* html
	cd html && touch .nojekyll
	cd html && git add .
	cd html && git commit -m 'Update gh-pages for $(MASTER_VERSION).'
	cd html && git push origin gh-pages

clean:
	rm -rf build dist html venv
	rm -rf doc/build
	rm -rf doc/venv
	rm -rf src/*.pyc
	rm -rf src/__pycache__
	rm -rf test/*.out
