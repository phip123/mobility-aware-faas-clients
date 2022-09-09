# Get IP from Pod in Zone A that hosts the app
IP=$(kubectl get pods -o json --selector app="mobilenet","ether.edgerun.io/zone"="zone-a" | jq '.items[] | .status.podIP' | sed 's/"//g')
etcdctl put golb/function/zone-a/mobilenet '{"ips": ["'${IP}':8080"], "weights":[100]}'

# Get IP from Pod in Zone B that hosts the app
IP=$(kubectl get pods -o json --selector app="mobilenet","ether.edgerun.io/zone"="zone-b" | jq '.items[] | .status.podIP' | sed 's/"//g')
etcdctl put golb/function/zone-b/mobilenet '{"ips": ["'"${IP}"':8080"], "weights":[100]}'


# Get IP from Pod in Zone C that hosts the app
IP=$(kubectl get pods -o json --selector app="mobilenet","ether.edgerun.io/zone"="zone-c" | jq '.items[] | .status.podIP' | sed 's/"//g')
etcdctl put golb/function/zone-c/mobilenet '{"ips": ["'${IP}':8080"], "weights":[100]}'
