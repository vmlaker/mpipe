# Shell script to build gh-pages.

# Start at the root directory.
cd ..

# Switch to gh-pages branch and start afresh.
git checkout gh-pages
rm -rf *

# Switch to master branch (Sphinx build needs doc/ test/ and src/.)
git checkout master doc test src
git reset HEAD

# Build the docs and move html/ files root directory.
cd doc
python ./create.py build
mv -fv build/html/* ..
cd ..

# Remove the directories (from master branch) needed for building docs.
rm -rf doc test src

# Add everything to gh-pages.
git add .

# Commit with comment referencing latest master branch commit.
git commit -m "Updated gh-pages for `git log master -1 | head -1`"

# Push.
#git push origin gh-pages
