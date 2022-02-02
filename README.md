# Deprecation Exporter


This tool is a very simple Python wrapper around the [`KubeNT`|https://github.com/doitintl/kube-no-trouble] binary. This tool exports Kubernetes API version deprecation information as Prometheus metris and are scrapped via a `servicemonitor`


Variables
`DEPRECATION_CHECK_WAIT_TIME`  The time, in seconds, between each scan. Default is `3600` (1 hour)
`METRICS_PORT`  The port that prometheus metrics server listens on. Default is `9092`
`METRICS_IP`    The IP to listen on for the prometheus metrics server. Defaul tis `0.0.0.0`


Helm 
```
helm repo add m-augustine https://m-augustine.github.io/deprecation-exporter
helm upgrade --install deprecation-exporter m-augustine/deprecation-exporter
```

Deploy
    Done through Cloudops CI