etcdctl put golb/function/zone-a/request_responder_250 '{"ips": ["10.0.3.1:8080"], "weights":[100]}'
etcdctl put golb/function/zone-b/request_responder_250 '{"ips": ["10.0.3.1:8080"], "weights":[100]}'

# Get IP from Pod that hosts the app
IP=$(kubectl get pods -o=jsonpath='{.items[?(@.metadata.labels.app=="request-responder-250")].status.podIP}')
etcdctl put golb/function/zone-c/request_responder_250 '{"ips": ["'"${IP}"':8080"], "weights":[100]}'
