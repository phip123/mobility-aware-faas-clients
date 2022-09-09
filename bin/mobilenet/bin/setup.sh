#!/usr/bin/env bash

echo "deploy pod"
kubectl apply -f bin/mobilenet/deployment/mobilenet-pod-zone-c.yaml

echo "wait till pods spawn"
kubectl wait --for=condition=ready pod -l app=mobilenet

echo "init etcd"
./bin/mobilenet/bin/init_etcd_load_balancer.sh
