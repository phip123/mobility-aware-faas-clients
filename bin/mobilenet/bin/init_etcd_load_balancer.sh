etcdctl put golb/function/zone-a/mobilenet '{"ips": ["10.0.3.1:8080"], "weights":[100]}'
etcdctl put golb/function/zone-b/mobilenet '{"ips": ["10.0.3.1:8080"], "weights":[100]}'

# Get IP from Pod that hosts the app
IP=$(kubectl get pods -o=jsonpath='{.items[?(@.metadata.labels.app=="mobilenet")].status.podIP}')
etcdctl put golb/function/zone-c/mobilenet '{"ips": ["'"${IP}"':8080"], "weights":[100]}'
