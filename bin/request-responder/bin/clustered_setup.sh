#!/usr/bin/env bash

echo "deploy pod in zone-c"
kubectl apply -f bin/request-responder/deployment/request-responder-pod-zone-c.yaml

echo "deploy pod in zone-a"
kubectl apply -f bin/request-responder/deployment/request-responder-pod-zone-a.yaml

echo "deploy pod in zone-b"
kubectl apply -f bin/request-responder/deployment/request-responder-pod-zone-b.yaml


echo "wait till pods spawn"
kubectl wait --for=condition=ready pod -l app=request-responder-250

echo "init etcd"
./bin/request-responder/bin/init_clustered_etcd_load_balancer.sh
