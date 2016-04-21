#!/bin/bash

# clear the coverage history
coverage erase

# build the coverage
FILES=`ls -1 tests/*.py | grep -v "__init__" | awk -F / '{print $2}' | grep -o '^[^\.]*'`
for f in $FILES; do
    coverage run --append --source models,controllers -m tests.$f > /dev/null
done

# display the coverage
coverage report -m
