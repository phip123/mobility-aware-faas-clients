#!/usr/bin/env bash

echo "deploy pod"
kubectl apply -f bin/request-responder/deployment/request-responder-pod-zone-c.yaml

echo "wait till pods spawn"
kubectl wait --for=condition=ready pod -l app=request-responder-250

echo "init etcd"
./bin/request-responder/bin/init_etcd_load_balancer.sh
