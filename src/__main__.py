#!/usr/bin/env python3

import json
import os
import subprocess
import prometheus_client as prom
import time



def kubent(helm2, helm3, cluster, targetVersion):
    cmd = ['kubent', '-o', 'json', '--helm2={}'.format(str(helm2)), '--helm3={}'.format(str(helm3)), '--cluster={}'.format(str(cluster)), '--target-version={}'.format(targetVersion)]

    result = subprocess.run(cmd, stdout=subprocess.PIPE)
    result = json.loads(result.stdout)

    return result

if __name__ == "__main__":
    sleepTime = os.getenv('DEPRECATION_CHECK_WAIT_TIME', "604800")
    targetVersion = os.getenv('TARGET_KUBERNETES_VERSION', "1.20.11")
    metricsPort = os.getenv('METRICS_PORT', "9092")
    metricsListenAddres = os.getenv('METRICS_IP', "0.0.0.0")


    prom.start_http_server(int(metricsPort), metricsListenAddres)

    gauge = prom.Gauge(
        "deprecation_in_cluster", 
        'Deprecation metric',
        ['name','namespace','kind','api_version','replace_with','since','source']
    )

    while True:
        # Look for HELM v2 resources only 
        for warning in kubent(True, False, False, targetVersion):
            value=(warning['RuleSet']).split()[-1]
            
            
            gauge.labels(
                warning['Name'],
                warning['Namespace'].replace('<undefined>','GLOBAL'),
                warning['Kind'],
                warning['ApiVersion'],
                warning['ReplaceWith'],
                warning['Since'],
                "helm2"
            
            ).set(value)

        # Look for HELM v3 resources only 
        for warning in kubent(False, True, False, targetVersion):
            value=(warning['RuleSet']).split()[-1]
            
            
            gauge.labels(
                warning['Name'],
                warning['Namespace'].replace('<undefined>','GLOBAL'),
                warning['Kind'],
                warning['ApiVersion'],
                warning['ReplaceWith'],
                warning['Since'],
                "helm3"
            
            ).set(value)

        # Look for Cluster resources only 
        for warning in kubent(False, False, True, targetVersion):
            value=(warning['RuleSet']).split()[-1]
            
            
            gauge.labels(
                warning['Name'],
                warning['Namespace'].replace('<undefined>','GLOBAL'),
                warning['Kind'],
                warning['ApiVersion'],
                warning['ReplaceWith'],
                warning['Since'],
                "cluster"
            
            ).set(value)

        time.sleep(int(sleepTime))