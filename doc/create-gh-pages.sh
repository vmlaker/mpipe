# Shell script to build gh-pages.

# Start at the root directory.
cd ..

# Switch to gh-pages branch and start afresh.
git checkout gh-pages
rm -rf *

# Switch to master branch (Sphinx build needs the checked out dirs and files).
git checkout master doc test src setup.py README.rst
git reset HEAD

# Create a Python Virtualenv.
virtualenv doc/venv
doc/venv/bin/python setup.py install
doc/venv/bin/pip install -r doc/requirements.txt

# Build the docs and move html/ files root directory.
cd doc

venv/bin/python ./create.py build
mv -fv build/html/* ..
cd ..

# Remove the directories (from master branch) needed for building docs.
rm -rf doc test src build README.rst setup.py

# Add everything to gh-pages.
git add --all .

# Commit with comment referencing latest master branch commit.
git commit -m "Updated gh-pages for `git log master -1 | head -1`"

# Push.
#git push origin gh-pages
