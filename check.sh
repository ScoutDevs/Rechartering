#!/bin/sh

flake8 .
pylint --rcfile=.pylintrc *.py
pylint --rcfile=.pylintrc aws
pylint --rcfile=.pylintrc models
pylint --rcfile=.pylintrc controllers
