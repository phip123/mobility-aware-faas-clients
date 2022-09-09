#!/usr/bin/env bash



if [ -z "$1" ]
then
      echo "No opt strategy passed passed..."
      exit 1
fi

if [ -z "$2" ]
then
      echo "No scenario chosen (single or clustered)"
      exit 1
fi

if [ -z "$3" ]
then
      echo "No run script passed..."
      exit 1
fi

OPT=$1
SCENARIO=$2
SCRIPT=$3

# initializes the etcd storage for the load balancer, executes the given script and then removes all created pods


if [ "$SCENARIO" = "single" ]; then
    echo "run single setup.sh"
    ./bin/request-responder/bin/setup.sh
elif [ "$SCENARIO" = "clustered" ]; then
    echo "run clustered setup.sh"
    ./bin/request-responder/bin/clustered_setup.sh
else
    echo "unknown scenario: $2"
    exit 1
fi

echo "run experiment $OPT $SCRIPT"
bash $SCRIPT $OPT

echo "run cleanup.sh"
./bin/request-responder/bin/cleanup.sh
