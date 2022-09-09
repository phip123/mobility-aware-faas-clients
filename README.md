# Osmotic Clients

This repo contains code that invokes the galileo shell to start experiments.

You can find executable run scripts under `bin`.

Environment variables
=====================

| Variable | Default |
|---|---|
| galileo_redis_host| localhost | 
| galileo_expdb_driver| mysql | 
| galileo_expdb_sqlite_path| ./philipp_galileo.sqlite | 
| galileo_logging_level| DEBUG | 
| galileo_expdb_mysql_host| localhost | 
| galileo_expdb_mysql_port| 3307 | 
| galileo_expdb_mysql_db| galileo | 
| galileo_expdb_mysql_user| galileo | 
| galileo_expdb_mysql_password| galileo | 
| galileo_expdb_influxdb_url| http://localhost:8086 | 
| galileo_expdb_influxdb_token| Jk05jlow2y1SZQePYk0-Iw3CNz1QuVgwWVdXhiucoTDMf-rYxKIR81JfNPfcfP7ua5Mb9o7oujuEH2bQ7Qus3w== | 
| galileo_expdb_influxdb_timeout| 10000 | 
| galileo_expdb_influxdb_org| galileo | 
| galileo_expdb_influxdb_org_id| a0ec9985b4a69119 | 
| KUBECONFIG | ~/.eb-k3s-config/k3s.yaml | 