#!/usr/bin/env bash

echo "deploy pod in zone-c"
kubectl apply -f bin/busy/deployment/busy-pod-zone-c.yaml

echo "deploy pod in zone-a"
kubectl apply -f bin/busy/deployment/busy-pod-zone-a.yaml

echo "deploy pod in zone-b"
kubectl apply -f bin/busy/deployment/busy-pod-zone-b.yaml


echo "wait till pods spawn"
kubectl wait --for=condition=ready pod -l app=busy

echo "init etcd"
./bin/busy/bin/init_clustered_etcd_load_balancer.sh
