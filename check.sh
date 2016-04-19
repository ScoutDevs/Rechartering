#!/bin/sh

flake8 .
pylint --rcfile=.pylintrc *.py
pylint --rcfile=.pylintrc aws
pylint --rcfile=.pylintrc models
pylint --rcfile=.pylintrc controllers
pylint --rcfile=.pylintrc tests
isort --recursive --quiet --force-single-line-imports --check-only
