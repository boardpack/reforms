#!/bin/sh -e
set -x

autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place reforms tests scripts --exclude=__init__.py
black reforms tests scripts
isort reforms tests scripts
