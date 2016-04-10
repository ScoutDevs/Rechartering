#!/bin/sh

python -m models.tests
python -m controllers.tests
#coverage run --source models
