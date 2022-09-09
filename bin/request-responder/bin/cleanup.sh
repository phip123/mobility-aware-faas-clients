#!/usr/bin/env bash

for pod in $(kubectl get pods -l ether.edgerun.io/function=request_responder_250 -o jsonpath='{.items..metadata.name}')
do
	kubectl delete pod $pod &
done
kubectl delete deployment telemd-kubernetes-adapter

wait
