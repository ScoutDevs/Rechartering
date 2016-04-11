#!/bin/sh

flake8 .
pylint *.py
pylint aws
pylint models
pylint controllers
