#!/usr/bin/env bash

set -o allexport
# shellcheck disable=SC1090
source ./bin/shell.env
set +o allexport

python -i -m galileo.cli.shell