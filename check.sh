#!/bin/sh

flake8 .
pylint .
pylint aws
pylint models
pylint controllers
