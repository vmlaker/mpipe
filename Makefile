.PHONY: venv

all: test

venv/bin/activate: requirements.txt
	test -d venv || virtualenv -p python3 venv
	. venv/bin/activate; pip install -Ur requirements.txt
	touch venv/bin/activate

venv: venv/bin/activate

test: venv
	./venv/bin/python setup.py build
	./venv/bin/python setup.py install
	./venv/bin/python setup.py test

docs: test
	cd doc && mkdir -p build/html
	cd doc && ../venv/bin/python create.py build

dist: clean venv
	./venv/bin/python setup.py sdist bdist_wheel

test_pypi: dist
	#./venv/bin/twine upload --repository testpypi dist/*
	./venv/bin/twine upload --repository-url https://test.pypi.org/legacy/ dist/*

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

# The "basic" (safe) level of cleanliness. Remove files of little consequence
# in a typical development flow.
clean1:
	rm -rf .coverage
	rm -rf .eggs/
	rm -rf .pytest_cache/
	rm -rf mpipe.egg-info/
	rm -rf src/__pycache__
	rm -rf src/*.pyc
	rm -rf test/__pycache__
	rm -rf test/*.out

clean: clean1
	rm -rf .python-version
	rm -rf build/
	rm -rf dist/
	rm -rf doc/build/
	rm -rf doc/venv
	rm -rf MANIFEST
	rm -rf venv/
