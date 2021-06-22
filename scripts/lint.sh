#!/usr/bin/env bash

set -e
set -x

mypy reforms
flake8 reforms tests
black reforms tests --check
isort reforms tests scripts --check-only
