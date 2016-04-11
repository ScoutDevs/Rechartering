#!/bin/sh

coverage run --source models,controllers tests.py && coverage report -m
