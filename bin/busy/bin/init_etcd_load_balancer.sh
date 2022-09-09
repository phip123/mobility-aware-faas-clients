etcdctl put golb/function/zone-a/busy '{"ips": ["10.0.3.1:8080"], "weights":[100]}'
etcdctl put golb/function/zone-b/busy '{"ips": ["10.0.3.1:8080"], "weights":[100]}'

# Get IP from Pod that hosts the app
IP=$(kubectl get pods -o=jsonpath='{.items[?(@.metadata.labels.app=="busy")].status.podIP}')
etcdctl put golb/function/zone-c/busy '{"ips": ["'"${IP}"':8080"], "weights":[100]}'
