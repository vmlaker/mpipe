#!/usr/bin/env bash

##############################################################
#
#  Install and setup pyenv to be used for platform builds.
#
##############################################################

#set -x  # Debugging.

# Install pyenv.
#rm -rf ~/.pyenv
#curl https://pyenv.run | bash
#cp bashrc_pyenv ~/.bashrc_pyenv
#echo . ~/.bashrc_pyenv >> ~/.bashrc

# Install pyenv-virtualenv plugin.
#git clone https://github.com/pyenv/pyenv-virtualenv.git $(pyenv root)/plugins/pyenv-virtualenv

# Load pyenv.
. bashrc_pyenv

# Install all versions used for testing.
#pyenv install 2.4.6
#pyenv install 2.5.6
#pyenv install 2.6.9
pyenv install 2.7.16
#pyenv install 3.1.5
#pyenv install 3.2.6
#pyenv install 3.3.7
pyenv install 3.4.10
pyenv install 3.5.7
pyenv install 3.6.8
pyenv install 3.7.3
pyenv install 3.8-dev

# Create a special virtualenv to be used for building MPipe.
pyenv virtualenv 3.6.8 mpipe_builder
pyenv shell mpipe_builder
pip install --upgrade pip
pip install -r requirements.txt

# Setup your Python stack for building all the versions
# while keeping the builder environment at the front. 
pyenv shell --unset
pyenv local \
      mpipe_builder 2.7.16 3.4.10 3.5.7 3.6.8 3.7.3 3.8-dev

# Run tox (see tox.ini).
tox
