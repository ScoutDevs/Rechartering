#!/bin/sh

coverage run --source models,controllers -m tests.model_tests
coverage run --append --source models,controllers -m tests.youth_application_controller_tests
coverage report -m
