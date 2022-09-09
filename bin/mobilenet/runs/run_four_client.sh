#!/usr/bin/env bash

set -o allexport
# shellcheck disable=SC1090
source ./bin/shell.env
set +o allexport

export osmotic_clients_scale_schedule_env_path=/root/praith/osmotic-loadbalancer-optimizer/bin/scale_schedule/$1.env

python -m clients.mobilenet.runs.fourclients bin/mobilenet/jsons/run_four_client.json