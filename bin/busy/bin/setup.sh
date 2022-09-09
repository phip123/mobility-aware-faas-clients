#!/usr/bin/env bash

echo "deploy pod"
kubectl apply -f bin/busy/deployment/busy-pod-zone-c.yaml

echo "wait till pods spawn"
kubectl wait --for=condition=ready pod -l app=busy

echo "init etcd"
./bin/busy/bin/init_etcd_load_balancer.sh
