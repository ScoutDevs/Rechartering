#!/bin/sh

flake8 .
pylint aws
pylint models
pylint controllers
