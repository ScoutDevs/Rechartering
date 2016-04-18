#!/bin/sh

coverage run --source models,controllers -m tests.all_models
coverage run --append --source models,controllers -m tests.youth_application_controller
coverage run --append --source models,controllers -m tests.youth_controller
coverage run --append --source models,controllers -m tests.organization_controller
coverage report -m
